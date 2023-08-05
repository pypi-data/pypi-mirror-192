"""Manage machines and domains."""

from __future__ import annotations

import configparser
import functools
import getpass
import io
import logging
import os
import pathlib
import subprocess
import tempfile
import textwrap
import time
from contextlib import contextmanager
from pathlib import Path

import newmath
import toml
import webagt
from rich.console import Console

from .. import templating
from . import providers

__all__ = ["spawn_machine", "Machine"]


console = Console()
templates = templating.templates(__name__)


def spawn_machine(name: str, host: providers.Host) -> Machine:
    """Spawn a new machine from given `host`."""
    key_path = Path("gaea_key")
    key_data = _get_key_data(key_path)
    for key in host.get_keys()["ssh_keys"]:
        if key["public_key"] == key_data:
            break
    else:
        key = host.add_key("gaea", key_data)
    machine = host.create_machine(name, ssh_keys=[key["id"]])
    ip_details = {}
    for ip_details in machine["networks"]["v4"]:
        if ip_details["type"] == "public":
            break
    return Machine(ip_details["ip_address"], "root", key_path)


def _get_key_data(key_path: Path):
    """Return a SSH key, creating one if necessary."""
    pubkey_path = key_path.with_suffix(".pub")
    if not pubkey_path.exists():
        subprocess.run(
            [
                "ssh-keygen",
                "-o",
                "-a",
                "100",
                "-t",
                "ed25519",
                "-N",
                "",
                "-f",
                str(pubkey_path)[:-4],
            ]
        )
    with pubkey_path.open() as fp:
        return fp.read().strip()


class MachineBase:
    """A cloud machine."""

    def __init__(self, address=None, user=None, key=None):
        """Return the machine at `address`."""
        if address is None:
            address = "localhost"
        self.address = address
        if user is None:
            user = getpass.getuser()
        self.user = user
        self.key = key
        self.run = self.get_ssh()
        self.system_dir = Path("/root")
        self.bin_dir = self.system_dir / "bin"
        self.etc_dir = self.system_dir / "etc"
        self.src_dir = self.system_dir / "src"
        self.var_dir = self.system_dir / "var"

    def get_ssh(self, output_handler=None):
        """Return a function for executing commands over SSH."""

        def ssh(*command, env=None, stdin=None):
            combined_env = os.environ.copy()
            if env:
                combined_env.update(env)
            kwargs = {
                "env": combined_env,
                "stderr": subprocess.STDOUT,
                "stdout": subprocess.PIPE,
            }
            if stdin:
                kwargs["stdin"] = subprocess.PIPE

            class Process:
                def __init__(self):
                    self.lines = []

                def __iter__(self):
                    for line in self.lines:
                        yield line

                @property
                def stdout(self):
                    return "\n".join(self.lines)

            process = Process()
            key_args = []
            if self.key:
                key_args = ["-i", self.key]
            with subprocess.Popen(
                ["ssh"]
                + key_args
                + [
                    "-tt",  # FIXME necessary?
                    "-o",
                    "IdentitiesOnly=yes",
                    "-o",
                    "StrictHostKeyChecking no",
                    f"{self.user}@{self.address}",
                    *command,
                ],
                **kwargs,
            ) as proc:
                if stdin:
                    try:
                        for line in proc.communicate(
                            input=stdin.encode("utf-8"), timeout=3
                        )[0].decode("utf-8"):
                            if output_handler:
                                output_handler(line)
                            else:
                                logging.debug(line)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                        stdout, stderr = proc.communicate()
                        logging.debug(f"stdout: {stdout}")
                        logging.debug(f"stderr: {stderr}")
                else:
                    for line in proc.stdout:
                        decoded_line = line.decode("utf-8").rstrip("\r\n")
                        process.lines.append(decoded_line)
                        logging.debug(decoded_line)
                        if output_handler:
                            output_handler(decoded_line)
            process.returncode = proc.returncode
            return process

        tries = 20
        while tries:
            result = ssh("true").returncode
            if result == 0:
                return ssh
            time.sleep(1)
            tries -= 1
        raise ConnectionError("SSH connection could not be made")

    def get(self, from_path, to_path=None):
        """"""

        def cp():
            self.cp(f"{self.user}@{self.address}:{from_path}", to_path)

        if to_path:
            cp()
        else:
            with tempfile.TemporaryDirectory() as tmpdirname:
                to_path = pathlib.Path(tmpdirname) / "alpha"
                cp()
                with to_path.open() as fp:
                    return fp.read()

    def send(self, from_path, to_path):
        """"""
        return self.cp(from_path, f"{self.user}@{self.address}:{to_path}")

    def cp(self, from_path, to_path):
        """Return a function for sending/retrieving a file over SCP."""
        with subprocess.Popen(
            [
                "scp",
                "-i",
                "gaea_key",
                "-o",
                "IdentitiesOnly=yes",
                "-o",
                "StrictHostKeyChecking=no",
                from_path,
                f"{self.user}@{self.address}:{to_path}",
            ],
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
        ) as process:
            for line in process.stdout:
                logging.debug(line.decode("utf-8"))
        return process

    def setup_machine(self):
        """Upgrade the system, install system packages and configure the firewall."""
        # NOTE debian 11.3->11.5 upgrading SSH kills connection
        # self._apt("dist-upgrade -yq", bg=True)  # TODO use cron to run upgrade(s)
        self._apt(f"install -yq {' '.join(self.system_packages)}")
        self.run("adduser gaea --disabled-login --gecos gaea")
        # TODO --shell /usr/bin/zsh"
        self.run("chmod 700 ~gaea")
        self.run(
            'echo "gaea  ALL=NOPASSWD: ALL" | tee -a /etc/sudoers.d/01_gaea'
        )  # XXX TODO FIXME !!!
        gaea_ssh_dir = "/home/gaea/.ssh"
        self.run(f"mkdir {gaea_ssh_dir}")
        self.run(f"cp /root/.ssh/authorized_keys {gaea_ssh_dir}")
        self.run(f"chown gaea:gaea {gaea_ssh_dir} -R")
        self.run(f"mkdir {self.src_dir} {self.etc_dir}")

    def open_ports(self, *ports):
        """Wall off everything but SSH and web."""
        self.run(
            "ufw allow proto tcp from any to any port "
            + ",".join([str(p) for p in ports])
        )
        self.run("ufw --force enable")

    def _apt(self, command, bg=False):
        time.sleep(1)  # the aptitude lock sometimes takes a second..
        command = f"apt-get -o DPkg::Lock::Timeout=60 {command}"
        if bg:
            command = f"nohup {command}"
        return self.run(command, env={"DEBIAN_FRONTEND": "noninteractive"})

    def _build(self, archive_url, *config_args):
        time.sleep(1)
        archive = Path(archive_url.rpartition("/")[2])
        with self.cd(self.src_dir) as src_dir:
            src_dir.run(f"wget https://{archive_url}")
            src_dir.run(f"tar xf {archive}")
            with src_dir.cd(archive.stem.removesuffix(".tar")) as archive_dir:
                archive_dir.run(f"bash ./configure {' '.join(config_args)}")
                archive_dir.run("make")
                archive_dir.run("make install")

    @contextmanager
    def cd(self, *directory_parts):
        """Return a context manager that changes the working directory."""
        directory = "/".join([str(p) for p in directory_parts])

        class Directory:
            run = functools.partial(self.run, f"cd {directory} &&")
            cd = functools.partial(self.cd, directory)

        yield Directory()

    @contextmanager
    def supervisor(self, local_conf_name, system_conf_name):
        """Return a context manager that provides access to Supervisor config files."""
        config = configparser.ConfigParser()
        yield config
        local_conf = f"{local_conf_name}.conf"
        output = io.StringIO()
        config.write(output)
        self.run(f"cat > {local_conf}", stdin=output.getvalue())
        self.run(f"ln -sf {local_conf} /etc/supervisor/conf.d/{system_conf_name}.conf")
        self.run("supervisorctl", "reread")
        self.run("supervisorctl", "update")


class Machine(MachineBase):
    """A full host in the cloud."""

    system_packages = (
        "build-essential",  # build tools
        "libbz2-dev",  # bz2 support
        "libicu-dev",
        "python3-icu",  # SQLite unicode collation
        "libsqlite3-dev",  # SQLite Python extension loading
        "python3-dev",  # Python build dependencies
        "cargo",  # rust (pycryptography)
        "libffi-dev",  # rust (pycryptography)
        "zlib1g-dev",
        "python3-cryptography",  # pycrypto
        "python3-libtorrent",  # libtorrent
        "zip",  # .zip support
        "expect",  # ssh password automation
        "psmisc",  # killall
        "xz-utils",  # .xz support
        "git",
        "fcgiwrap",  # Git w/ HTTP serving
        "supervisor",  # service manager
        # XXX "redis-server",  # Redis key-value database
        "haveged",  # produces entropy for faster key generation
        "sqlite3",  # SQLite flat-file relational database
        "libssl-dev",  # uWSGI SSL support
        "ffmpeg",  # a/v en/de[code]
        "imagemagick",  # heic -> jpeg
        "libsm-dev",
        # TODO "python3-opencv",  # computer vision  # NOTE lots of packages...
        # XXX "libevent-dev",  # Tor
        "pandoc",  # markup translation
        "graphviz",  # graphing
        "brotli",  # wasm build for DT
        "libgtk-3-0",
        "libdbus-glib-1-2",  # Firefox
        "xvfb",
        "tmux",
        "x11-utils",  # browser automation
        "libenchant-2-dev",  # pyenchant => sopel => bridging IRC
        "tmux",  # automatable terminal multiplexer
        "tree",
        "htop",
        "stow",  # for dotfiles
        "zsh",  # default shell
    )
    versions = {
        "python": "3.10.9",
        # "firefox": "97.0",
        # "geckodriver": "0.27.0",
    }
    ssl_ciphers = ":".join(
        (
            "ECDHE-RSA-AES256-GCM-SHA512",
            "DHE-RSA-AES256-GCM-SHA512",
            "ECDHE-RSA-AES256-GCM-SHA384",
            "DHE-RSA-AES256-GCM-SHA384",
            "ECDHE-RSA-AES256-SHA384",
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nginx_dir = self.system_dir / "nginx"
        self.python_dir = self.system_dir / "python"
        self.runinenv = self.system_dir / "runinenv"
        self.projects_dir = self.system_dir / "projects"

    def setup_python(self):
        """
        Install Python (w/ SQLite extensions) for application runtime.

        Additionally create a `runinenv` for running things inside virtual environments.

        """
        self._build(
            "python.org/ftp/python/{0}/Python-{0}.tar.xz".format(
                self.versions["python"]
            ),
            # TODO "--enable-optimizations",  # NOTE adds 9 minutes
            "--enable-loadable-sqlite-extensions",
            f"--prefix={self.python_dir}",
        )
        self.run(
            f"cat > {self.runinenv}",
            stdin=textwrap.dedent(
                """\
                #!/usr/bin/env bash
                VENV=$1
                . ${VENV}/bin/activate
                shift 1
                exec "$@"
                deactivate"""
            ),
        )
        self.run(f"chmod +x {self.runinenv}")

    def setup_admin(self):
        """Install administrative interface."""
        self.run("/root/python/bin/python3 -m venv admin")
        self.run("runinenv admin pip install webint")

    def setup_tor(self):
        """Install Tor for anonymous routing."""
        self._apt("install -yq tor")
        self.torrc = "/etc/tor/torrc"
        self.tor_data = "/var/lib/tor"
        self.run(
            f"cat > {self.torrc}",
            stdin=textwrap.dedent(
                f"""\
                HiddenServiceDir {self.tor_data}/main
                HiddenServicePort 80 127.0.0.1:80"""
            ),
        )
        self.run("service tor restart")
        self.onion = self.get(f"{self.tor_data}/main/hostname")

    def setup_nginx(self):
        """
        Install Nginx (w/ TLS, HTTPv2, RTMP) for web serving.

        """
        self._apt("install -yq nginx libnginx-mod-rtmp")
        self.nginx_conf = "/etc/nginx/nginx.conf"
        self.web_data = "/var/www"
        self.open_ports(80, 443)
        protected_path = newmath.nbrandom(5)
        self.run(f"mkdir {self.web_data}")
        self.run(
            f"cat > {self.web_data}/{protected_path}.html",
            stdin=str(templates.nginx_index(self.address)),
        )
        self.run(
            f"cat > {self.nginx_conf}",
            stdin=str(templates.nginx_conf(self.address, self.onion)),
        )
        self.run("service nginx restart")
        self.generate_dhparam(512)  # NOTE 2048 adds ? minutes
        return protected_path

    # def setup_node(self):
    #     """Install Node from NodeSource."""
    #     ...

    def generate_dhparam(self, bits=4096):
        """Generate a unique Diffie-Hellman prime for Nginx."""
        self.run(f"openssl dhparam -out {self.system_dir}/dhparam.pem {bits}")

    def install_project(self, registrar, project_root=Path(".")):
        """Install sites from project in `project_root`."""
        # TODO install from Git URL
        with (project_root / "pyproject.toml").open() as fp:
            project = toml.load(fp)["tool"]["poetry"]
        try:
            sites = project["plugins"]["websites"]
        except KeyError:
            console.print("No sites found in `pyproject.toml`.")
            return
        name = project["name"]
        wheel = sorted((project_root / "dist").glob("*.whl"))[-1].name
        console.print(f"Installing project `{name}`")
        project_dir = self.projects_dir / name
        env_dir = f"{project_dir}/env"
        data_dir = f"{project_dir}/data"
        dist_dir = f"{project_dir}/dist"
        certs_dir = f"{project_dir}/certs"
        challenges_dir = f"{project_dir}/certs/challenges"

        # self.run(f"mkdir {data_dir} {dist_dir} {challenges_dir} -p")
        # self.run(f"{self.python_dir}/bin/python3 -m venv {env_dir}")
        # self.cp(f"dist/{wheel}", dist_dir)
        # self.run(f"{self.runinenv} {env_dir} pip install {dist_dir}/{wheel}")
        with self.supervisor(f"{self.projects_dir}/{name}", name) as config:
            for domain, obj in sites.items():
                domain = domain.replace("_", ".")
                console.print(f"Pointing https://{domain} to `{obj}`")
                d = webagt.uri.parse(domain)
                registrar.create_record(
                    f"{d.domain}.{d.suffix}", self.address, d.subdomain
                )
                config[f"program:{domain}-app"] = {
                    "autostart": "true",
                    "command": (
                        f"{self.runinenv} {env_dir} gunicorn {obj} "
                        f"-k gevent -w 2 --bind unix:{project_dir}/gunicorn.sock"
                    ),
                    "directory": data_dir,
                    "stopsignal": "INT",
                    "user": "root",
                }
                # config[f"program:{domain}-jobs"] = {
                #     "autostart": "true",
                #     "command": f"{self.runinenv} {env_dir} loveliness serve",
                #     "directory": data_dir,
                #     "stopsignal": "INT",
                #     "user": "root",
                # }
                # TODO create non-TLS nginx config for let's encrypting domain
                # TODO reload nginx
                # TODO initiate let's encrypt flow
                # TODO replace non-TLS nginx config with TLS-based config
                # TODO reload nginx
                local_nginx = project_dir / "nginx.conf"
                system_nginx = self.nginx_dir / f"conf/conf.d/project_{name}.conf"
                print("local", local_nginx)
                print("system", system_nginx)
                C = str(templates.nginx_site(domain, project_dir, self.ssl_ciphers))
                print(C)
                self.run(
                    f"cat > {local_nginx}",
                    stdin=C,
                )
                self.run(f"ln -sf {local_nginx} {system_nginx}")

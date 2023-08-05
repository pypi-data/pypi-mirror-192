"""Command line tools for the web."""

import inspect
import json
import logging
import pathlib
import webbrowser

import txt
import webagt
from rich.pretty import pprint

import web
import web.host
from web.host import console, providers

__all__ = ["main"]


main = txt.application("web", web.__doc__)
config_file = pathlib.Path("~/.webint").expanduser()


def get_config():
    """Get configuration."""
    try:
        with config_file.open() as fp:
            config = json.load(fp)
    except FileNotFoundError:
        config = {}
    return config


def update_config(**items):
    """Update configuration."""
    config = get_config()
    config.update(**items)
    with config_file.open("w") as fp:
        json.dump(config, fp, indent=2, sort_keys=True)
        fp.write("\n")
    return get_config()


@main.register()
class Apps:
    """Show installed web apps."""

    def run(self, stdin, log):
        for pkg, apps in web.get_apps().items():
            for name, _, ns, obj in apps:
                print(f"{name} {ns}:{obj[0]}")
        return 0


@main.register()
class Fnord:
    def run(self, stdin, log):
        # import asyncio
        # asyncio.run(web.serve("web:abba", port=9999))
        web.StandaloneServer(web.abba, 9999).run()


@main.register()
class Dev:
    """Develop a web app locally."""

    def setup(self, add_arg):
        add_arg("app", help="name of web application")
        add_arg("--port", help="port to serve on")
        add_arg("--socket", help="file socket to serve on")
        add_arg("--watch", default=".", help="directory to watch for changes")

    def run(self, stdin, log):
        import asyncio

        if self.port:
            asyncio.run(web.serve(self.app, port=self.port, watch_dir=self.watch))
        elif self.socket:
            asyncio.run(web.serve(self.app, socket=self.socket, watch_dir=self.watch))
        else:
            print("must provide a port or a socket")
            return 1
        return 0

        # for pkg, apps in web.get_apps().items():
        #     for name, _, ns, obj in apps:
        #         if self.app == name:
        #             web.serve(ns, obj)
        #             return 0
        # return 1


def get_providers(provider_type):
    return [
        name.lower()
        for name, obj in inspect.getmembers(providers, inspect.isclass)
        if issubclass(obj, provider_type) and obj is not provider_type
    ]


@main.register()
class Config:
    """Config your environments."""

    def setup(self, add_arg):
        add_arg("token", help="API access token")
        add_arg(
            "--host",
            choices=get_providers(providers.Host),
            help="machine host",
        )
        add_arg(
            "--registrar",
            choices=get_providers(providers.Registrar),
            help="domain registrars",
        )

    def run(self, stdin, log):
        if self.host:
            update_config(host=self.host, host_token=self.token)
        elif self.registrar:
            update_config(registrar=self.registrar, registrar_token=self.token)
        return 0


@main.register()
class Bootstrap:
    """Bootstrap a cloud machine."""

    def run(self, stdin, log):
        logging.basicConfig(
            level=logging.DEBUG,
            filename="debug.log",
            filemode="w",
            force=True,
            format="%(levelname)s:%(asctime)s:%(name)s:%(message)s",
        )
        config = get_config()

        if config["host"] == "digitalocean":
            host = providers.DigitalOcean(config["host_token"])
        elif config["host"] == "linode":
            host = providers.Linode(config["host_token"])
        else:
            console.print(f"Host {config['host']} not available.")
            return 1

        # if config["registrar"] == "dynadot":
        #     registrar = providers.Dynadot(config["registrar_token"])
        # elif config["registrar"] == "linode":
        #     registrar = providers.Linode(config["registrar_token"])
        # else:
        #     console.print(f"Registrar {config['registrar']} not available.")
        #     return 1

        machines = config.get("machines", [])
        if len(machines) == 0:
            console.print("No machines found")
            versions = web.host.Machine.versions
            with console.status(
                "[bold green]Creating new machine ([magenta]12 min[/magenta] total)"
            ):
                console.print(
                    f"Spawning virtual machine at {host.__class__.__name__} "
                    "([magenta]1 min[/magenta])"
                )
                machine = web.host.spawn_machine("website", host)
                machine._apt("update")
                machine._apt("install -yq ufw")
                machine.open_ports(22)
                console.print(f"Installing tor..")
                protected_path = machine.setup_tor()
                console.print(f"Installing nginx.. ([magenta]1 min[/magenta])")
                protected_path = machine.setup_nginx()
                webbrowser.open(f"http://{machine.address}/{protected_path}")
                console.print("Setting up system.. ([magenta]3 min[/magenta])")
                machine.setup_machine()
                console.print(f"Installing python.. ([magenta]5 min[/magenta])")
                machine.setup_python()
                console.print(
                    f"Installing admin interface.. ([magenta]5 min[/magenta])"
                )
                machine.setup_admin()
                machines.append(machine.address)
                update_config(machines=machines)
        machine = web.host.Machine(machines[0], "root", "gaea_key")
        console.rule(f"[green]Using {machine.address}")
        # with console.status("[bold blue]Installing/upgrading sites"):
        #     machine.install_project(registrar)
        return 0


@main.register()
class Host:
    """Manage your host."""

    def run(self, stdin, log):
        config = get_config()
        if config["host"] == "digitalocean":
            host = providers.DigitalOcean(config["host_token"])
        else:
            console.print(f"Host {config['host']} not available.")
            return 1
        for machine in host.machines:
            console.rule(f"[bold red]{machine['name']}")
            pprint(machine)
        return 0


@main.register()
class Registrar:
    """Manage your registrar."""

    def run(self, stdin, log):
        config = get_config()
        if config["registrar"] == "dynadot":
            registrar = providers.Dynadot(config["registrar_token"])
        else:
            console.print(f"Registrar {config['registrar']} not available.")
            return 1
        for domain in registrar.domains:
            print(domain)
        return 0


if __name__ == "__main__":
    main()

# nuitka-project: --include-package=gevent.signal
# nuitka-project: --include-package=gunicorn.glogging
# nuitka-project: --include-package=gunicorn.workers.sync
# nuitka-project: --include-package=web.framework.templates
# nuitka-project: --include-package=web.host.templates
# nuitka-project: --include-package-data=mf2py
# nuitka-project: --include-package-data=selenium

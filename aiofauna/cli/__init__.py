import asyncio
import functools
import os
import pathlib
import signal
import socket
import subprocess
import sys
import traceback
from typing import Any

import click
from aiohttp.web import run_app
from aiohttp_devtools import __version__
from aiohttp_devtools.cli import cli
from aiohttp_devtools.exceptions import AiohttpDevException
from aiohttp_devtools.logs import main_logger, setup_logging
from aiohttp_devtools.runserver import INFER_HOST
from aiohttp_devtools.runserver import runserver as _runserver
from aiohttp_devtools.runserver import serve_static

from .build import main as build_main
from .curl import main as curl_main
from .git import main as git_main
from .kill import main as kill_main

_dir_existing = click.Path(exists=True, dir_okay=True, file_okay=False)
_file_dir_existing = click.Path(exists=True, dir_okay=True, file_okay=True)
_dir_may_exist = click.Path(
    dir_okay=True, file_okay=False, writable=True, resolve_path=True
)


verbose_help = "Enable verbose output."
livereload_help = (
    "Whether to inject livereload.js into html page footers to autoreload on changes. "
    "env variable AIO_LIVERELOAD"
)


static_help = "Path of static files to serve, if excluded static files aren't served. env variable: AIO_STATIC_STATIC"
root_help = (
    "Root directory project used to qualify other paths. "
    "This can be used to watch a parent directory for changes in a more complex application. "
    "env variable: AIO_ROOT"
)
static_url_help = 'URL path to serve static files from, default "/static/". env variable: AIO_STATIC_URL'
host_help = (
    "host used when referencing livereload and static files, if blank host is taken from the request header "
    "with default of localhost. env variable AIO_HOST"
)
app_factory_help = (
    "name of the app factory to create an aiohttp.web.Application with, if missing default app-factory "
    "names are tried. This can be either a function with signature "
    '"def create_app(loop): -> Application" or "def create_app(): -> Application" '
    "or just an instance of aiohttp.Application. env variable AIO_APP_FACTORY"
)
port_help = "Port to serve app from, default 8000. env variable: AIO_PORT"
aux_port_help = "Port to serve auxiliary app (reload and static) on, default port + 1. env variable: AIO_AUX_PORT"

def gen_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@click.group()
@click.version_option(__version__, "-V", "--version")
@click.option("-v", "--verbose", is_flag=True, help=verbose_help)
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """
    AioFauna CLI
    """
    setup_logging(verbose=verbose)
    ctx.obj = {}

    if verbose:
        main_logger.debug("Verbose mode enabled")


# defaults are all None here so default settings are defined in one place: DEV_DICT validation
@main.command()
@click.argument(
    "app-path",
    envvar="AIO_APP_PATH",
    type=_file_dir_existing,
    required=False,
    default=".",
)
@click.option(
    "-s",
    "--static",
    "static_path",
    envvar="AIO_STATIC_PATH",
    type=_dir_existing,
    help=static_help,
    default="./static",
)
@click.option(
    "--root",
    "root_path",
    envvar="AIO_ROOT",
    type=_dir_existing,
    help=root_help,
    default=".",
)
@click.option(
    "--static-url", envvar="AIO_STATIC_URL", help=static_url_help, default="/"
)
@click.option(
    "--livereload/--no-livereload",
    envvar="AIO_LIVERELOAD",
    default=True,
    help=livereload_help,
)
@click.option("--host", default=INFER_HOST, help=host_help)
@click.option(
    "-p",
    "--port",
    "main_port",
    envvar="AIO_PORT",
    type=click.INT,
    help=port_help,
    default=8080,
)
@click.option(
    "--app-factory", "app_factory_name", envvar="AIO_APP_FACTORY", help=app_factory_help
)
@click.option(
    "--aux-port",
    envvar="AIO_AUX_PORT",
    type=click.INT,
    help=aux_port_help,
    default=gen_port(),
)
@click.option("-v", "--verbose", is_flag=True, help=verbose_help, default=True)
@click.argument("project_args", nargs=-1)
def dev(**config: Any) -> None:
    """
    Run a development server for aiofauna/aiohttp apps.

    Takes one argument "app-path" which should be a path to either a directory containing a recognized default file
    ("app.py" or "main.py") or to a specific file. Defaults to the environment variable "AIO_APP_PATH" or ".".

    The app path is run directly, see the "--app-factory" option for details on how an app is loaded from a python
    module.
    """
    active_config = {k: v for k, v in config.items() if v is not None}
    setup_logging(config["verbose"])
    # Rewrite argv for the application.
    sys.argv[1:] = active_config.pop("project_args")
    try:
        run_app(**_runserver(**active_config))
    except AiohttpDevException as e:
        if config["verbose"]:
            tb = click.style(traceback.format_exc().strip("\n"), fg="white", dim=True)
            main_logger.warning("AiohttpDevException traceback:\n%s", tb)
        main_logger.error("Error: %s", e)
        sys.exit(2)


@main.command()
def prod():
    """
    Run a production server for aiofauna/aiohttp apps.
    """
    subprocess.check_output(["python", "main.py"])
    

@main.command()
def build():
    """
    Build project
    """
    build_main()


@main.command()
def git():
    """
    Push to git
    """
    git_main()


@main.command()
def kill():
    """
    Kill port
    """
    kill_main()
    
@main.command()
def curl():
    """
    Run curl
    """
    curl_main()
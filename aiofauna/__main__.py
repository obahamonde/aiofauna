import os
import subprocess

import click

from .utils import setup_logging

logger = setup_logging(__name__)

print = logger.debug


@click.group()
def main():
    pass


def print_tree(dirname, pref=""):
    for item in os.listdir(dirname):
        if item.startswith("."):
            continue
        print(pref + item)
        if os.path.isdir(os.path.join(dirname, item)):
            logger.info(
                os.path.join(dirname, item), " " * len(pref) + "|" + ("_" * 5) + " "
            )


@main.command()
def tree():
    """Prints the directory tree of the current working directory."""
    print_tree(os.getcwd())


@main.command()
@click.option(
    "--port",
    default=8080,
    type=int,
    help="Port in which the application will listen for requests.",
)
@click.option(
    "--host",
    default="0.0.0.0",
    type=str,
    help="Host that will run the application process.",
)
@click.option(
    "--reload",
    default=True,
    flag_value=True,
    help="When enabled, the server will reload on change.",
)
@click.option(
    "--worker",
    default=1,
    type=int,
    help="Number of workers to spawn. This is the number of processes that will be spawned.",
)
@click.option(
    "--threads",
    default=1,
    type=int,
    help="Number of threads to spawn. This is the number of threads that will be spawned per worker.",
)
@click.argument("name", default="main:app", type=str, nargs=1, required=False)
def run(name, port, host, reload, worker, threads):
    """Spins up a Gunicorn server which serves the app.\n
    It comes with the following options:\n
     --port: Port to run the server on\n
     --host: Host to run the server on\n
     --reload: Reload the server on change\n
     --worker: Number of workers to spawn\n
     --threads: Number of threads to utilize\n\n

     name: Name of the app to run it comes in the format of <module>:<app>, where module is the name of your entry point file without the extension and app is the name of the global variable which contains the `APIServer` instance.\n\n

     Example: aiofauna run main:app --port 5000 --host 0.0.0.0 --reload --worker 1 --threads 1 (This is the default configuration BTW, when you just execute `aiofauna run`)
    """
    subprocess.run(
        [
            "gunicorn",
            "-b",
            f"{host}:{port}",
            "-k",
            "aiohttp.worker.GunicornWebWorker",
            "--reload" if reload else "",
            "--workers",
            str(worker),
            "--threads",
            str(threads),
            name,
        ],
        check=True,
    )

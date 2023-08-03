import os
import subprocess

import click

from .utils import setup_logging

logger = setup_logging(__name__)


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
    print_tree(os.getcwd())


@main.command()
@click.option("--port", default=5000)
@click.option("--host", default="0.0.0.0")
@click.option("--reload", default=True)
@click.option("--worker", default=1)
@click.option("--threads", default=1)
@click.argument("name")
def run(name, port, host, reload, worker, threads):
    subprocess.run(
        [
            "gunicorn",
            "-b",
            f"{host}:{port}",
            "--reload" if reload else "",
            "--workers",
            str(worker),
            "--threads",
            str(threads),
            name,
        ],
        check=True,
    )

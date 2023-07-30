import os
import sys

import click

from .logging import setup_logging

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
    
                                                            
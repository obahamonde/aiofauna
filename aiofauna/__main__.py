import os
import subprocess
import logging
import click
import shutil
from rich.console import Console
from rich.logging import RichHandler
from rich.pretty import install
from rich.traceback import install as ins


def setup_logging(name: str) -> logging.Logger:
    """
    Set's up logging using the Rich library for pretty and informative terminal logs.

    Arguments:
    name -- Name for the logger instance. It's best practice to use the name of the module where logger is defined.
    """
    install()
    ins()
    console = Console(record=True, force_terminal=True)
    console_handler = RichHandler(
        console=console,
        show_time=True,
        show_path=True,
        markup=True,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        tracebacks_extra_lines=2,
        tracebacks_theme="monokai",
        show_level=False,
    )
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    console_handler.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO, handlers=[console_handler])
    logger_ = logging.getLogger(name)
    logger_.setLevel(logging.INFO)
    return logger_


logger = setup_logging(__name__)
print = logger.info


@click.group()
def main():
    pass


def print_tree(dirname, pref=""):
    for item in os.listdir(dirname):
        if item.startswith("."):
            continue
        if item == os.listdir(dirname)[-1]:
            print(f"{pref}└── {item}")
            if os.path.isdir(os.path.join(dirname, item)):
                print_tree(os.path.join(dirname, item), pref + "    ")
        else:
            print(f"{pref}├── {item}")
            if os.path.isdir(os.path.join(dirname, item)):
                print_tree(os.path.join(dirname, item), pref + "│   ")


@main.command()
def tree():
    """Prints the directory tree of the current working directory."""
    print_tree(os.getcwd())


@main.command()
def rmcache():
    """Removes all __pycache__ directories in the current working directory and its subdirectories."""
    for root, dirs, files in os.walk(os.getcwd()):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            print(f"Removing {pycache_path}")
            shutil.rmtree(pycache_path)


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


if __name__ == "__main__":
    main()

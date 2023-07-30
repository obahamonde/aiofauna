"""Logging and error handling utilities for the OpenAI Function Python package."""
import logging
from typing import Any, Callable, Coroutine, TypeVar

from aiohttp.web_exceptions import HTTPException
from rich.console import Console
from rich.logging import RichHandler
from rich.pretty import install
from rich.traceback import install as ins

# Typing the return type of the wrapped function.
T = TypeVar("T")


def setup_logging(name: str) -> logging.Logger:
    """
    Set's up logging using the Rich library for pretty and informative terminal logs.

    Arguments:
    name -- Name for the logger instance. It's best practice to use the name of the module where logger is defined. # pylint: disable=line-too-long
    """

    # Install pretty representations of data structures using Rich library.
    install()

    # Install Rich traceback handler.
    ins()

    # Create a Console object that can record terminal output.
    console = Console(record=True, force_terminal=True)

    # Create a RichHandler for rich logging.
    console_handler = RichHandler(
        console=console,
        show_time=True,
        show_path=True,
        markup=True,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        tracebacks_extra_lines=5,
        tracebacks_theme="solarized",
    )

    # Set the log level and formatter for the console handler.
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    console_handler.setLevel(logging.INFO)

    # Setup basic configuration for logging.
    logging.basicConfig(level=logging.INFO, handlers=[console_handler])

    # Create and return a logger with the specified name.
    logger_ = logging.getLogger(name)
    logger_.setLevel(logging.INFO)

    return logger_


# Set up a logger for this module.
logger = setup_logging(__name__)


def handle_errors(
    func: Callable[..., Coroutine[Any, Any, T]]
) -> Callable[..., Coroutine[Any, Any, T]]:  # pylint: disable=line-too-long
    """
    A decorator to handle errors in an asynchronous function.

    Arguments:
    func -- The asynchronous function whose errors are to be handled.
    """

    async def wrapper(*args: Any, **kwargs: Any) -> T:
        """
        Wrapper function to handle errors in the function call.
        """
        try:
            logger.info("Calling %s", func.__name__)
            return await func(*args, **kwargs)
        except HTTPException as exc:
            logger.error(exc.__class__.__name__)
            logger.error(exc.reason)
            raise exc from exc
        except Exception as exc:
            logger.error(exc.__class__.__name__)
            logger.error(str(exc))
            raise exc from exc

    return wrapper


def log(cls):
    """Adds a logger to a class."""
    if not hasattr(cls, "logger"):
        cls.logger = setup_logging(cls.__name__)
    return cls

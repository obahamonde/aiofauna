"""Logging and error handling utilities for the OpenAI Function Python package."""
import functools
import logging
from time import perf_counter
from typing import Any, Callable, Coroutine, Generator, Sequence, TypeVar, cast

from aiohttp.web_exceptions import HTTPException
from rich.console import Console
from rich.logging import RichHandler
from rich.pretty import install
from rich.traceback import install as ins
from typing_extensions import ParamSpec

T = TypeVar("T")
P = ParamSpec("P")


def setup_logging(name: str) -> logging.Logger:
    """
    Set's up logging using the Rich library for pretty and informative terminal logs.

    Arguments:
    name -- Name for the logger instance. It's best practice to use the name of the module where logger is defined. # pylint: disable=line-too-long
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
    console_handler.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG, handlers=[console_handler])
    logger_ = logging.getLogger(name)
    logger_.setLevel(logging.DEBUG)
    return logger_


logger = setup_logging(__name__)


def process_time(
    func: Callable[P, Coroutine[Any, Any, T]]
) -> Callable[..., Coroutine[Any, Any, T]]:  # pylint: disable=line-too-long
    """
    A decorator to measure the execution time of an asynchronous function.

    Arguments:
    func -- The asynchronous function whose execution time is to be measured.
    """

    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        """
        Wrapper function to time the function call.
        """
        start = perf_counter()
        result = await func(*args, **kwargs)
        end = perf_counter()
        logger.info("Time taken to execute %s: %s seconds", func.__name__, end - start)
        return result

    return wrapper


def handle_errors(
    func: Callable[P, Coroutine[Any, Any, T]]
) -> Callable[P, Coroutine[Any, Any, T]]:  # pylint: disable=line-too-long
    """
    A decorator to handle errors in an asynchronous function.

    Arguments:
    func -- The asynchronous function whose errors are to be handled.
    """

    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
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


def chunker(seq: Sequence[T], size: int) -> Generator[Sequence[T], None, None]:
    """
    A generator function that chunks a sequence into smaller sequences of the given size.

    Arguments:
    seq -- The sequence to be chunked.
    size -- The size of the chunks.
    """
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


def gen_emptystr() -> str:
    return cast(str, None)

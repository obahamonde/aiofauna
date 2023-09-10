"""zLogging and error handling utilities for the OpenAI Function Python package."""
import functools
import logging
from time import perf_counter
from typing import Any, Callable, Coroutine, Generator, Sequence, TypeVar, cast
from aiohttp.web_response import Response
from aiohttp.web_exceptions import HTTPException
from rich.console import Console
from rich.logging import RichHandler
from rich.pretty import install
from rich.traceback import install as ins
from typing import Optional
from typing_extensions import ParamSpec
from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name
from jinja2 import Environment, FileSystemLoader, Template
from .exceptions import EXCEPTIONS

T = TypeVar("T")
P = ParamSpec("P")


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


def process_time(
    func: Callable[P, Coroutine[Any, Any, T]]
) -> Callable[P, Coroutine[Any, Any, T]]:
    """
    A decorator to measure the execution time of a coroutine.

    Arguments:
    func -- The coroutine whose execution time is to be measured.
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
) -> Callable[P, Coroutine[Any, Any, T]]:
    """
    A decorator to handle errors in a coroutine.

    Arguments:
    func -- The coroutine whose errors are to be handled.
    """

    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        """
        Wrapper function to handle errors in the function call.
        """
        try:
            return await func(*args, **kwargs)
        except EXCEPTIONS as exc:
            logger.error(exc.__class__.__name__)
            logger.error(str(exc))
            raise HTTPException(reason=str(exc)) from exc

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
    """
    A generator function that returns an empty string.
    """
    return cast(str, None)


def highlight_code(code, lang, opts, env):
    """
    A function that highlights code using pygments.
    """
    if not lang:
        lang = "md"
    lexer = get_lexer_by_name(lang, stripall=True)
    formatter = HtmlFormatter(**opts)
    return highlight(code, lexer, formatter)


def highlight_code(code: str, lang: str, _options: dict) -> str:
    if not lang:
        lexer = get_lexer_by_name("md")
    lexer = get_lexer_by_name(lang)
    style = get_style_by_name("monokai")
    formatter = HtmlFormatter(style=style)
    return highlight(code, lexer, formatter)


def render_markdown(markdown: str) -> str:
    markdownit = MarkdownIt(
        "js-default",
        {
            "html": True,
            "linkify": True,
            "typographer": True,
            "highlight": highlight_code,
            "renderer": RendererHTML(),
        },
    )
    return markdownit.render(markdown)

import functools
from typing import Optional

from aiohttp.web import HTTPException, Request, Response, StreamResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2.exceptions import (
    TemplateAssertionError,
    TemplateError,
    TemplateNotFound,
    TemplateSyntaxError,
    UndefinedError,
)
from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
from markdown_it.rules_block import StateBlock
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import MarkdownLexer, get_lexer_by_name

from ..utils import setup_logging

EXCEPTIONS = (
    TemplateAssertionError,
    TemplateError,
    TemplateNotFound,
    TemplateSyntaxError,
    UndefinedError,
    Exception,
)

logger = setup_logging(__name__)


def handle_template(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except EXCEPTIONS as e:
            logger.error(e)
            raise HTTPException(reason=str(e)) from e

    return wrapper


class HighlightRenderer(RendererHTML):
    def code_block(self, tokens, idx, options, env):
        token = tokens[idx]
        lexer = get_lexer_by_name(token.info.strip() if token.info else "text")
        formatter = HtmlFormatter()
        return highlight(token.content, lexer, formatter)


def highlight_code(code, name, attrs):
    """Highlight a block of code"""
    lexer = get_lexer_by_name(name)
    formatter = HtmlFormatter()

    return highlight(code, lexer, formatter)


class ServerSideRenderer(StreamResponse):
    def __init__(
        self,
        headers={"Content-Type": "text/html"},
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, headers=headers, **kwargs)
        self.env = Environment(
            loader=FileSystemLoader("templates"),
            autoescape=select_autoescape(["html", "xml", "jinja2", "md"]),
            enable_async=True,
        )
        self.md = MarkdownIt(
            "js-default",
            options_update={
                "html": True,
                "linkify": True,
                "typographer": True,
                "highlight": highlight_code,
            },
        )

    @handle_template
    async def render_markdown(self, template_name: str, request: Request, **context):
        await self.prepare(request)
        template = self.env.get_template(template_name)
        response = self.md.render(await template.render_async(**context))
        for chunk in response:
            await self.write(chunk.encode())
        await self.write_eof()
        return self

    @handle_template
    async def stream_markdown(self, template_name: str, request: Request, **context):
        await self.prepare(request)
        template = self.env.get_template(template_name)
        async for chunk in template.generate_async(**context):
            await self.write(self.md.render(chunk).encode())
        await self.write_eof()
        return self

    @handle_template
    async def render_template(self, template_name: str, request: Request, **context):
        await self.prepare(request)
        template = self.env.get_template(template_name)
        response = await template.render_async(**context)
        for chunk in response:
            await self.write(chunk.encode())
        await self.write_eof()
        return self

    @handle_template
    async def stream_template(self, template_name: str, request: Request, **context):
        await self.prepare(request)
        template = self.env.get_template(template_name)
        async for chunk in template.generate_async(**context):
            await self.write(chunk.encode())
        await self.write_eof()
        return self

    @handle_template
    async def markdown_string(self, string: str, request: Request):
        await self.prepare(request)
        response = self.md.render(string)
        for chunk in response:
            await self.write(chunk.encode())
        await self.write_eof()
        return self

    @handle_template
    async def stream_markdown_string(self, string: str, request: Request):
        await self.prepare(request)
        for chunk in string:
            await self.write(self.md.render(chunk).encode())
        await self.write_eof()
        return self

    @handle_template
    async def render_html(self, string: str, request: Request):
        await self.prepare(request)
        for chunk in string:
            await self.write(chunk.encode())
        await self.write_eof()
        return self

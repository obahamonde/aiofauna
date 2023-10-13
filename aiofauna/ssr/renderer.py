import os

import pkg_resources
from jinja2 import (ChoiceLoader, Environment, FileSystemLoader,
                    select_autoescape)
from markdown_it import MarkdownIt  # type: ignore
from markdown_it.renderer import RendererHTML  # type: ignore
from pydantic import BaseConfig  # pylint: disable=no-name-in-module
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pydantic import (BaseSettings, Extra,  # pylint: disable=no-name-in-module
                      Field)
from pygments import highlight  # type: ignore
from pygments.formatters.html import HtmlFormatter  # type: ignore
from pygments.lexers import get_lexer_by_name  # type: ignore
from pygments.styles import get_style_by_name  # type: ignore


def highlight_code(code: str, lang: str, _) -> str:
    """
    A function to highlight code using pygments.

    Arguments:
    code -- The code to be highlighted.
    lang -- The language of the code.
    """
    lexer = get_lexer_by_name(lang, stripall=True)
    formatter = HtmlFormatter(  # type: ignore
        style=get_style_by_name("github-dark"),  # type: ignore
    )  # type: ignore
    return highlight(code, lexer, formatter)  # type: ignore


def render_markdown(text: str) -> str:
    """
    A function to render markdown using markdown-it.

    Arguments:
    text -- The markdown text to be rendered.
    """
    md = MarkdownIt(renderer_cls=RendererHTML)
    md.options.html = True
    md.options.linkify = True
    md.options.typographer = True
    md.options.breaks = True
    md.options.highlight = highlight_code
    return md.render(text)


class SSRSettings(BaseSettings):
    """Default settings for Static Site Generator"""

    class Config(BaseConfig):
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = Extra.allow

    STATIC_DIR: str = Field(
        default_factory=lambda: os.path.join(os.getcwd(), "static"), env="STATIC_DIR"
    )
    TEMPLATE_DIR: str = Field(
        default_factory=lambda: os.path.join(os.getcwd(), "templates"),
        env="TEMPLATE_DIR",
    )
    MARKDOWN_DIR: str = Field(
        default_factory=lambda: os.path.join(os.getcwd(), "markdown"),
        env="MARKDOWN_DIR",
    )


class SSRRenderer(BaseModel):
    """
    A class for Rendering Static Site Generator templates.

    Attributes:
            title (str): The title for the site. Default is "AioFaunaSSG".

    .. note::
            This class uses Pydantic for data validation.

    """

    title: str = Field(default="AioFaunaSSG")

    class Config(BaseConfig):
        extra = Extra.allow
        arbitrary_types_allowed = True


    @property
    def loader(self) -> ChoiceLoader:
        """
        Returns a ChoiceLoader for the Jinja2 Environment.

        Returns:
                ChoiceLoader: A loader that can load templates from multiple sources.
        """
        templates_loader = FileSystemLoader(SSRSettings().TEMPLATE_DIR)
        layouts_loader = FileSystemLoader(
            pkg_resources.resource_filename("aiofauna", "ssg/layouts")
        )
        markdown_loader = FileSystemLoader(SSRSettings().MARKDOWN_DIR)

        return ChoiceLoader([templates_loader, layouts_loader, markdown_loader])

    @property
    def settings(self) -> SSRSettings:
        """
        Returns the settings for the SSG.

        Returns:
                SSGSettings: The settings for the SSG.
        """
        return SSRSettings()

    @property
    def jinja_env(self) -> Environment:
        """
        Returns a Jinja2 Environment.

        Returns:
                Environment: The Jinja2 Environment for template rendering.
        """
        return Environment(
            loader=self.loader,
            autoescape=select_autoescape(["html", "xml", "md", "markdown"]),
            enable_async=True,
        )

    async def render_html(self, template: str) -> str:
        """
        Renders a template using Jinja2.

        Args:
                template (str): The name of the template file.

        Returns:
                str: The rendered HTML as a string.
        """
        return await self.jinja_env.get_template(template).render_async(**self.dict())

    async def render_markdown(
        self, template: str, layout: str = "md_layout.html"
    ) -> str:
        """
        Renders a markdown file using a layout.

        Args:
                template (str): The name of the markdown file.
                layout (str, optional): The layout to use. Defaults to "md_layout.html".

        Returns:
                str: The rendered HTML as a string.
        """
        content = await self.render_html(template)
        return await self.jinja_env.get_template(layout).render_async(
            title=self.title, content=render_markdown(content)
        )
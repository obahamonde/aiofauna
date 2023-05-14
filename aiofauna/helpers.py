"""
Flaskaesque helper functions for aiohttp.
"""
import re
from markdown import markdown  # pylint: disable=import-error
from aiohttp import web
from aiofauna import Response
from pygments import highlight
from pygments.formatters import HtmlFormatter  # pylint: disable=no-name-in-module
from pygments.lexers import get_lexer_by_name
from jinja2 import Environment, FileSystemLoader, select_autoescape

MD_FMT_CDN = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css/github-markdown.min.css">"""  # pylint: disable=line-too-long
CODE_FMT_CDN = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pygments-css@1.0.0/github.min.css">"""  # pylint: disable=line-too-long

html_formatter = HtmlFormatter(style="default")

jinja_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
    extensions=["jinja2.ext.do"],
)

md_env = Environment(
    loader=FileSystemLoader("markdown"),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def markdown_it(md_string: str):
    """
    Render a markdown file to HTML.

    Args:
        md_string (str): The markdown file to render.

    Returns:
        str: The rendered HTML.
    """

    template = md_env.get_template(md_string)
    text = template.render()
    code = re.findall(r"```[a-z]*\n[\s\S]*?\n```", text)
    for code_ in code:
        lang = re.findall(r"```([a-z]*)\n", code_)[0]
        lexer = get_lexer_by_name(lang)
        code = re.findall(r"```[a-z]*\n([\s\S]*?)\n```", code_)[0]
        code = highlight(code, lexer, html_formatter)
        text = text.replace(code_, code)
    text = markdown(text, extensions=["fenced_code"])
    text = f"""
    <html>
        <head>
            <meta charset="utf-8">
            {MD_FMT_CDN}
            {CODE_FMT_CDN}
        </head>
        <style>
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 40px;
            text-align: center;
            font-weight: 600;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}
        </style>
        <body class="markdown-body">
        <main class="container">
            {text}
        </main>
        </body>
    </html>
    """
    return Response(text=text, content_type="text/html")


def redirect(url):
    """
    Create an HTTP redirect response.

    Args:
        url (str): The URL to redirect to.

    Returns:
        web.HTTPFound: An HTTP redirect response with the specified URL.
    """

    return web.HTTPFound(url)


def make_response(data, headers=None, status=200):
    """
    Create an HTTP response with the given data, headers, and status code.

    Args:
        data (str): The response body data.
        headers (dict, optional): A dictionary of headers to include in the response. Defaults to None.
        status (int, optional): The HTTP status code for the response. Defaults to 200.

    Returns:
        web.Response: An HTTP response with the specified data, headers, and status code.
    """
    return web.Response(body=data, headers=headers, status=status)


def render_template(template_name, **kwargs):
    """
    Render an HTML template with the given context variables and return an HTTP response.

    Args
        template_name (str): The name of the template file.
        **kwargs: Keyword arguments representing context variables to be passed to the template.

    Returns:
        web.Response: An HTTP response with the rendered template as its body and content type set to "text/html".
    """
    template = jinja_env.get_template(template_name).render(**kwargs)
    return web.Response(body=template.encode(), content_type="text/html")

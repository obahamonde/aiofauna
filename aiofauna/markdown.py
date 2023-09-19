"""Markdown component decorator for Jinja2 templates."""
import jinja2
import typing_extensions
import typing
from typing import Any, Callable, Coroutine
import functools
import asyncio
from .utils import render_markdown

T = typing.TypeVar("T")
P = typing_extensions.ParamSpec("P")

MD_TOP="""
<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Docs</title>
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/default.min.css">

</head>
<style type="text/css">
	.markdown-body {
		box-sizing: border-box;
		min-width: 200px;
		max-width: 980px;
		margin: 0 auto;
		padding: 45px;
	}

	@media (max-width: 767px) {
		.markdown-body {
			padding: 15px;
		}
	}
</style>


<body>
	<div class="markdown-body">
"""

MD_BOTTOM="""
</div>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
	<script src="https://cdn.jsdelivr.net/npm/@unocss/runtime/mini.global.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/htmx/1.9.5/htmx.min.js"
		integrity="sha512-2NwoAICmYEIEuayBZdfd/cEvYGevbb1jezvQli/Iw052KfAA3NGrXAH2AY02cjt3gMdui5Q8nKauPYgVOE+pmg=="
		crossorigin="anonymous" referrerpolicy="no-referrer"></script>
	<script>
		hljs.highlightAll();
	</script>
</body>

</html>
"""

def markdown(
    func: Callable[P, Coroutine[Any, Any, T]]
) -> Callable[P, Coroutine[Any, Any, T]]:
    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        if asyncio.iscoroutinefunction(func):
            md = render_markdown(await func(*args, **kwargs))
        else:
            md = render_markdown(func(*args, **kwargs))
        template_str =jinja2.Template(
            MD_TOP + md + MD_BOTTOM
    )
        return template_str.render()

    return wrapper

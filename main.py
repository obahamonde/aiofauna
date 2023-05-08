"""AioFauna Documentation as an example of markdown handler."""
from aiofauna import Api, markdown_it

app = Api()


@app.get("/")
async def md_handler():
    """Aiofauna Docs"""
    return markdown_it("index.md")

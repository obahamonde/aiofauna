from aiofauna import ASGIApi

app = ASGIApi()


@app.get("/")
async def index():
    """Renders the index page"""
    return "Hello World"


from aiofauna import Api

app = Api()


@app.get("/")
async def index():
    """Renders the index page"""
    return "Hello World"



from aiofauna.cli.curl import HttpClient

h = HttpClient()

print(h.get("http://localhost:8000/"))
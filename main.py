from aiofauna import APIServer, HTTPFound


app = APIServer()

@app.get("/")
async def index():
	return HTTPFound("/index.html")


app.router.add_static("/","./docs/_build/html")
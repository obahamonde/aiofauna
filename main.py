from aiofauna import *

DOCKER_URL = "http://localhost:9898"

HEADERS = {
	"Content-Type": "application/json",
}

class Item(FaunaModel):
	name: str
	price: float
	is_offer: bool = None


app = APIServer()

docker = APIClient(base_url=DOCKER_URL, headers=HEADERS)

@app.post("/items")
async def create_item(item: Item):
	return await item.create()


@app.get("/items/{ref}")
async def get_item(ref: str):
	return await Item.get(ref)


@app.get("/images")
async def get_images():
	response = await docker.get("/images/json?all=1")
	app.logger.info(response)
	return response
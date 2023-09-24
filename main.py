from aiohttp import ClientSession

from aiofauna import APIServer, Client, FaunaModel, HTTPFound, json
from aiofauna.api import injectable


class JSONPlaceHolder(Client):
	...	

class User(FaunaModel):
	...

api = JSONPlaceHolder(base_url="https://jsonplaceholder.typicode.com")

app = APIServer()

client = Client(base_url="https://jsonplaceholder.typicode.com")

@app.get("/")
async def index():
	return await client.request("GET", "/posts")


@app.get("/users")
async def users():
	return await User.all()
from aiofauna import *
from uuid import uuid4
app = APIServer()

@app.get("/")
@md_component()
def index():
	"""# AioFauna: a Backend Framework that Scales
## What is AioFauna?
AioFauna is a backend framework that scales. It is designed to be used with FaunaDB, a serverless database that scales automatically. AioFauna is built on top of AioHTTP, a high-performance asynchronous HTTP server and client. AioFauna is opinionated and batteries included like Django, but it is also designed to be modular and extensible like Flask, while providing the performance and developer experience of FastAPI.
## Why AioFauna?
Finding the right database for your project is hard. You need to consider the performance, scalability, and cost of the database. You also need to consider the developer experience of the database. AioFauna is designed to provide a great developer experience while also providing a database that scales automatically. Distributed as a Data API through a global CDN, FaunaDB is a serverless database that scales automatically. It is designed to be used with AioFauna out of the box.
## How do I get started?
You can get started with AioFauna by installing it with pip:
```bash
pip install aiofauna
```
You can then create a new `main.py` file with the following code:
```python
from aiofauna import APIServer

app = APIServer()

@app.get("/")
def index():
  return "Hello World!"
```

**NOTE**: you will need `FAUNA_SECRET` in your environment variables to run this code.

You can then run the server with:

`aiofauna run`

You can then visit http://localhost:8080/ to see the result. Or you can visit http://localhost:8080/docs to see the documentation.

# Creating a basic CRUD API

You can create a basic CRUD API by creating a new `main.py` file with the following code:

```python

from aiofauna import APIServer, FaunaModel, Field

class User(FaunaModel):
  name: str = Field()
  email: str = Field(unique=True)

app = APIServer()

@app.get("/")
async def index():
  return await User.all()

@app.post("/")
async def create_user(user: User):
  return await user.save()

@app.get("/{id}")
async def get_user(id: str):
  return await User.find(id)

@app.put("/{id}")
async def update_user(id: str, age: int):
  return await user.update(id, age=age)

@app.delete("/{id}")
async def delete_user(id: str):
  return await User.delete(id)


```

You can visit the `swagger` documentation at http://localhost:8080/docs to test the endpoints.

	"""

	return {}



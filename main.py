from aiofauna import ASGIServer, FaunaModel, Field
from mangum import Mangum


class Person(FaunaModel):
	name: str = Field(...)
	age: int = Field(...)


app = ASGIServer()



@app.get("/")
async def index():
	return {"hello": "world"}

@app.get("/users")
async def users():
	return await Person.all()

@app.post("/users")
async def create_user(person: Person):
  return await person.save()

@app.get("/users/{id}")
async def get_user(id: str):
	return await Person.get(id)

@app.put("/users/{id}")
async def update_user(id: str, age: int):
	return await Person.update(id, age=age)

@app.delete("/users/{id}")
async def delete_user(id: str):
	return await Person.delete(id)



handler = Mangum(app)
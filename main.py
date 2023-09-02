from aiofauna import *
from src import *


class Catalog(FaunaModel):
    name:str
    data:str

app = APIServer(servers=["http://localhost:8080"])



@app.get("/api/")
async def catalog():
    return [s.openaischema for s in OpenAIFunction.Metadata.subclasses]


@app.get("/api")
async def chat(text: str):
    return await function_call(text=text)

@app.post("/api/{text}")
async def momo(text: str):
    return await Catalog(name=text, data=text).save()

@app.get("/api/catalog")
async def catalog_all():
    return await Catalog.all()

@app.get("/api/catalog/{id}")
async def catalog_get(id: str):
    return await Catalog.get(id)

@app.delete("/api/catalog/{id}")
async def catalog_del(id: str):
    return await Catalog.delete(id)

@app.put("/api/catalog/{id}")
async def catalog_put(id: str, data: str):
    return await Catalog.update(id,data=data)

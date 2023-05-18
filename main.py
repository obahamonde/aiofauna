import inspect

import models
from aiofauna import Api, render_template
from aiofauna.asgi import aioasgi
from mixins import *


@app.get("/api/auth")
async def auth(token: str):
    """Authenticates a user"""
    data = await client.fetch(
        f"https://{env.AUTH0_DOMAIN}/userinfo", headers={"Authorization": f"Bearer {token}"}
    )
    return await User(**data).save()

@app.delete("/api/upload")
async def delete_upload(ref: str):
    """Delete an uploaded file given it's document reference"""
    await Upload.delete(ref)
    return {"message": "Asset deleted successfully", "status": "success"}


@app.get("/api/upload")
async def get_upload(user: str):
    """Fetch Uploaded files for a given user"""
    return await Upload.find_many("user", user)


@app.get("/api/users")
async def get_users():
    """Fetch all users"""
    return await User.all()


@app.get("/")
async def index():
    """Renders the index page"""
    return render_template("index.html")

app.static()


@app.on_event("startup")
async def startup(_) -> None:
    """Runs on startup"""
    _models = [o for n, o in inspect.getmembers(models) if inspect.isclass(o) and issubclass(o, FaunaModel) and o != FaunaModel]
    await asyncio.gather(*[m.provision() for m in _models])
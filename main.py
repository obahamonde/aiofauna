from aiofauna import Api
from mixins import *


@app.get("/")
async def index():
    """Health check endpoint"""
    return {"message": "Accepted", "status": "success"}


@app.get("/api/auth")
async def auth(token: str):
    """Authenticates a user"""
    data = await client.fetch(
        f"https://{env.AUTH0_DOMAIN}/userinfo", headers={"Authorization": f"Bearer {token}"}
    )
    return await Auth0User(**data).save()


#@app.on_event("startup")
async def startup(_) -> None:
    """Runs on startup"""
    import models
    import inspect
    _models = [o for n, o in inspect.getmembers(models) if inspect.isclass(o) and issubclass(o, FaunaModel)]
    await asyncio.gather(*[m.provision() for m in _models])
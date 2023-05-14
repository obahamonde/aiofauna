import asyncio
from aiofauna import (
    FaunaModel,
    Api,
    BaseModel,
    Field,
    Optional as O,
    Dict as D,
    List as L,
    Any as A,
    Union as U,
    Callable as C,
)
from aiofauna.helpers import render_template, markdown_it, redirect
from aiofauna.client import HTTPClient
from aiofauna.query import index

AUTH0_URL = "https://dev-tvhqmk7a.us.auth0.com"

client = HTTPClient()


class Auth0User(FaunaModel):
    """Auth0 User"""

    email: O[str] = Field(default=None, index=True)
    email_verified: O[bool] = Field(default=False)
    family_name: O[str] = Field(default=None)
    given_name: O[str] = Field(default=None)
    locale: O[str] = Field(default=None, index=True)
    name: str = Field(...)
    nickname: O[str] = Field(default=None)
    picture: O[str] = Field(default=None)
    sub: str = Field(...)
    updated_at: O[str] = Field(default=None)


class Message(FaunaModel):
    """Message"""

    text: str = Field(..., index=True)
    user: str = Field(..., index=True)
    kind: O[str] = Field(
        default="TEXT", oneOf=["TEXT", "IMAGE", "VIDEO", "AUDIO"], index=True
    )
    conversation: O[str] = Field(default=None, unique=True)


class Conversation(FaunaModel):
    """Messages"""

    messages: L[str] = Field(default=[])
    users: L[str] = Field(default=[])


app = Api()


@app.get("/")
async def index_():
    """Health check endpoint"""
    return {"message": "Accepted", "status": "success"}


@app.get("/api/auth")
async def auth(token: str):
    """Authenticates a user"""
    data = await client.fetch(
        f"{AUTH0_URL}/userinfo", headers={"Authorization": f"Bearer {token}"}
    )
    return await Auth0User(**data).save()


@app.on_event("startup")
async def startup(_) -> None:
    """Runs on startup"""
    await Auth0User.provision()
    await Message.provision()
    await Conversation.provision()

import asyncio
from aiofauna import (
    FaunaModel,
    BaseModel,
    Field,
    Optional as O,
    Dict as D,
    List as L,
    Any as A,
    Union as U,
    Callable as C,
)
from aiofauna.api import UploadFile


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
    users: L[str] = Field(default=[], max_items=2, unique=True)


class GroupChat(FaunaModel):
    """Messages"""

    messages: L[str] = Field(default=[])
    users: L[str] = Field(default=[], max_items=100)

class UserUpload(FaunaModel):
    """User Upload"""

    user: str = Field(..., index=True)
    file: UploadFile = Field(..., index=True)
    url: O[str] = Field(default=None, unique=True)
    kind: O[str] = Field(
        default="IMAGE", oneOf=["IMAGE", "VIDEO", "AUDIO"], index=True
    )

class UserMessages(BaseModel):
    """User Messages"""

    conversation: str
    user: Auth0User
    messages: L[Message]
    

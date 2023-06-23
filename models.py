import asyncio
from datetime import datetime
from typing import Any as A
from typing import Callable as C
from typing import Dict as D
from typing import List as L
from typing import Optional as O
from typing import Union as U

from aiofauna import BaseModel, FaunaModel, Field


class User(FaunaModel):
    """Auth0 User"""

    email: O[str] = Field(default=None, index=True)
    email_verified: O[bool] = Field(default=False)
    family_name: O[str] = Field(default=None)
    given_name: O[str] = Field(default=None)
    locale: O[str] = Field(default=None, index=True)
    name: str = Field(...)
    nickname: O[str] = Field(default=None)
    picture: O[str] = Field(default=None)
    sub: str = Field(..., unique=True)
    updated_at: O[str] = Field(default=None)
    is_online: O[bool] = Field(default=False, index=True)


class Message(FaunaModel):
    """Message"""

    text: str = Field(..., index=True)
    user: str = Field(..., index=True)
    kind: O[str] = Field(
        default="TEXT", oneOf=["TEXT", "IMAGE", "VIDEO", "AUDIO"], index=True
    )
    conversation: str = Field(..., index=True)
    read: O[bool] = Field(default=False, index=True)


class Conversation(FaunaModel):
    """Messages"""

    name: O[str] = Field(default=None, unique=True)
    owner: str = Field(..., index=True)
    guest: str = Field(..., index=True)
    messages: L[Message] = Field(default_factory=list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.name:
            self.name = f"{self.owner}-{self.guest}"


class Upload(FaunaModel):
    """

    R2 Upload Record

    """

    user: str = Field(..., description="User sub", index=True)
    name: str = Field(..., description="File name")
    key: str = Field(..., description="File key")
    size: int = Field(..., description="File size", gt=0)
    type: str = Field(..., description="File type", index=True)
    lastModified: float = Field(
        default_factory=lambda: datetime.now().timestamp(),
        description="Last modified",
        index=True,
    )
    url: O[str] = Field(None, description="File url")


class Invitation(FaunaModel):
    """Invitation"""

    sender: str = Field(..., index=True)
    receiver: str = Field(..., index=True)
    hashed: O[str] = Field(default=None, unique=True)
    status: O[str] = Field(default="PENDING", oneOf=["PENDING", "ACCEPTED", "REJECTED"], index=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.hashed:
            self.hashed = self.hash(self.sender, self.receiver)

    def hash(self, sender: str, receiver: str) -> str:
        """Hashes the sender and receiver"""
        return f"{sender}-{receiver}"
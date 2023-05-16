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
from datetime import datetime

class Wuser(FaunaModel):
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
    name:O[str] = Field(default=None, unique=True)
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
    size: int = Field(..., description="File size",gt=0)
    type: str = Field(..., description="File type", index=True)
    lastModified: float = Field(default_factory=lambda: datetime.now().timestamp(), description="Last modified", index=True)
    url: O[str] = Field(None, description="File url")
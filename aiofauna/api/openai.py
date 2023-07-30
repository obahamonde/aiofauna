"""Chat Completions Schemas"""
from typing import List, Literal, NamedTuple

Role = Literal["assistant", "user", "system", "function"]
Model = Literal["gpt-4-0613", "gpt-3.5-turbo-16k-0613"]


class Message(NamedTuple):
    """Defines a message within a conversation."""

    role: Role
    content: str


class ChatCompletionRequest(NamedTuple):
    """Defines a request for a chat completion."""

    model: Model
    messages: List[Message]
    temperature: float
    max_tokens: int
    stream: bool


class ChatCompletionUssage(NamedTuple):
    """Defines the usage of the tokens for a chat completion."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionChoice(NamedTuple):
    """Defines a choice in a chat completion."""

    index: int
    message: Message
    finish_reason: str


class ChatCompletionResponse(NamedTuple):
    """Defines a response for a chat completion."""

    id: str
    object: str
    created: int
    model: Model
    choices: List[ChatCompletionChoice]
    usage: ChatCompletionUssage 
    stream: bool

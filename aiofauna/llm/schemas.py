"""Chat Completions Schemas"""
from typing import List, Literal, NamedTuple, Union

import numpy as np

from ..odm import FaunaModel

Vector = Union[np.ndarray, List[float]]

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


class VectorResponse(NamedTuple):
    text: str
    score: float


class Embedding(FaunaModel):
    """Defines an embedding."""

    vector: Vector
    namespace: str
    text: str

    async def similarity_search(
        self, vector: Vector, namespace: str, limit: int = 1000, k: int = 10
    ) -> List[VectorResponse]:
        """
        Searches for similar embeddings.

        Args:
            vector: The vector to search for.
            namespace: The namespace to search in.
            limit: The maximum number of results to return.
            k: The number of results to return per query.

        Returns:
            A list of VectorResponse.
        """
        results = await self.find_many(limit=limit, namespace=namespace)
        similarities = [
            VectorResponse(text=result.text, score=result.similarity(vector))
            for result in results
        ]
        return sorted(similarities, key=lambda x: x.score, reverse=True)[:k]

    def similarity(self, vector: Vector):
        return (np.dot(self.vector, vector)) / (
            (np.linalg.norm(self.vector) * np.linalg.norm(vector))
        )

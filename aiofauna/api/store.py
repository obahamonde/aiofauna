import json
import os
from typing import Any, AsyncGenerator, List, NamedTuple, Type
from uuid import uuid4

import openai
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pydantic import Field  # pylint: disable=no-name-in-module
from tqdm import tqdm

from ..client import APIClient, APIException
from ..logging import handle_errors, log, setup_logging
from ..typedefs import (F, FunctionRequest, FunctionType, Message, MetaData,
                        Model, Optional, Vector)
from .openai import List, Literal

logger = setup_logging(__name__)


class Math(FunctionType):
    """Math operation between two numbers."""

    a: float = Field(..., description="First number.")
    b: float = Field(..., description="Second number.")
    operation: Literal[
        "add", "subtract", "multiply", "divide", "power", "root"
    ] = Field(..., description="Operation to perform.")
    result: Optional[float] = Field(
        default=None, description="Result of the operation."
    )

    async def run(self):
        """Run the function."""
        if self.operation == "add":
            self.result = self.a + self.b
        elif self.operation == "subtract":
            self.result = self.a - self.b
        elif self.operation == "multiply":
            self.result = self.a * self.b
        elif self.operation == "divide":
            self.result = self.a / self.b
        elif self.operation == "power":
            self.result = self.a**self.b
        elif self.operation == "root":
            self.result = self.a ** (1 / self.b)
        else:
            raise ValueError(f"Invalid operation: {self.operation}")
        return self.result


class UpsertVector(NamedTuple):
    id: str = Field(default_factory=lambda: str(uuid4()))
    values: Vector = Field(...)
    metadata: MetaData = Field(...)


class UpsertRequest(NamedTuple):
    vectors: List[UpsertVector]
    namespace: str


class UpsertResponse(NamedTuple):
    upsertedCount: int


class QueryRequest(NamedTuple):
    topK: int
    namespace: str
    vector: Vector
    includeMetadata: bool


class QueryMatch(NamedTuple):
    id: str
    score: float
    values: Vector
    metadata: MetaData


class QueryResponse(NamedTuple):
    matches: List[QueryMatch]
    namespace: str
    results: int


class IngestRequest(NamedTuple):
    namespace: str
    texts: List[str]



class LLMStack(APIClient):
    base_url = os.environ.get("PINECONE_URL")  # type: ignore
    headers = {"api-key": os.environ.get("PINECONE_API_KEY")}  # type: ignore

    @handle_errors
    async def upsert_vectors(self, request: UpsertRequest) -> UpsertResponse:
        response = await self.fetch(
            "/vectors/upsert", method="POST", json=request._asdict()
        )
        return UpsertResponse(**response)

    @handle_errors
    async def query_vectors(self, request: QueryRequest) -> QueryResponse:
        response = await self.fetch(
            "/query", method="POST", json=request._asdict())
        return QueryResponse(**response)

    @handle_errors
    async def upsert_messages(
        self,
        user_embedding: Vector,
        openai_embedding: Vector,
        prompt: str,
        text: str,
        namespace: str,
    ) -> None:
        upsert_request = UpsertRequest(
            vectors=[
                UpsertVector(values=user_embedding, metadata={"text": prompt}),
                UpsertVector(values=openai_embedding, metadata={"text": text}),
            ],
            namespace=namespace,
        )
        await self.upsert_vectors(upsert_request)

    @handle_errors
    async def chat(self, text: str, context: str) -> str:
        """Chat completion with no functions."""
        messages = [
            {"role": "user", "content": text},
            {"role": "system", "content": context},
        ]
        logger.info("Chat messages: %s", messages)
        response = await openai.ChatCompletion.acreate(
            model="gpt-4-0613", messages=messages
        )
        logger.info("Chat response: %s", response)
        assert isinstance(response, dict)
        return response["choices"][0]["message"]["content"]

    @handle_errors
    async def chat_with_memory(self, text: str, namespace: str, context: str) -> str:
        """Chat completion with similarity search retrieval from pinecone"""
        try:
            embedding = await self.create_embeddings(text)
            query_request = QueryRequest(vector=embedding, namespace=namespace, topK=3, includeMetadata=True)
            query_response = await self.query_vectors(query_request)
            similar_text_chunks = [
                i.get("metadata", {}).get("text", "") for i in query_response.matches
            ]
            similar_text = "Previous Similar results:" + "\n".join(similar_text_chunks)
            messages = [
                {"role": "user", "content": text},
                {"role": "system", "content": similar_text},
                {"role": "system", "content": context},
            ]
            logger.info("Chat messages: %s", messages)
            response = await openai.ChatCompletion.acreate(
                model="gpt-4-0613",
                messages=messages,
            )
            return response["choices"][0]["message"]["content"]
        except Exception as exc:
            logger.exception(exc)
            raise APIException(message=str(exc)) from exc

    @handle_errors
    async def chat_with_functions(
        self,
        text: str,
        context: Optional[str] = None,
        functions: List[Type[F]] = FunctionType._subclasses,
    ) -> Any:
        """Chat completion with functions."""
        return await function_call(text, context=context, functions=functions)

    @handle_errors
    async def create_embeddings(self, text: str) -> Vector:
        """Creates embeddings for the given texts."""
        response = await openai.Embedding.acreate(
            model="text-embedding-ada-002",
            input=text,
        )
        return response["data"][0]["embedding"]

    async def chat_stream(self, text: str) -> AsyncGenerator[str, None]:
        """Chat completion stream with no functions."""
        response = openai.ChatCompletion.acreate(
            model="gpt-4-0613",
            messages=[{"role": "user", "content": text}],
            stream=True,
        )
        async for i in response:
            assert isinstance(i, dict)
            delta = i["choices"][0]["delta"]
            if "content" in delta:
                yield delta["content"]

    async def chat_stream_with_memory(
        self, text: str, namespace: str = "default"
    ) -> AsyncGenerator[str, None]:
        """Chat completion stream with similarity search retrieval from pinecone"""
        try:
            embedding = await self.create_embeddings(text)
            query_request = QueryRequest(vector=embedding, namespace=namespace, topK=3, includeMetadata=True)
            query_response: QueryResponse = await self.query_vectors(query_request)
            logger.info("# of matches: %s", len(query_response.matches))  # type: ignore
            similar_text_chunks = [
                i.metadata.get("text", "") for i in query_response.matches
            ]
            similar_text = "Previous Similar results:" + "\n".join(similar_text_chunks)
            response = openai.ChatCompletion.acreate(
                model="gpt-4-0613",
                messages=[
                    {"role": "user", "content": text},
                    {"role": "system", "content": similar_text},
                ],
                stream=True,
            )
            assert isinstance(response, AsyncGenerator)
            async for i in response:
                assert isinstance(i, dict)
                delta = i["choices"][0]["delta"]
                if "content" in delta:
                    yield delta["content"]
        except Exception as exc:
            logger.exception(exc)
            raise APIException(message=str(exc)) from exc

    @handle_errors
    async def chatgpt(
        self, text: str, context: str, namespace: str = "default", memory: bool = False
    ):
        """ChatGPT4 is a function that allows you to chat with GPT-4, with the option of using memory or functions."""
        if memory:
            return await self.chat_with_memory(
                text=text, namespace=namespace, context=context
            )
        return await self.chat(text=text, context=context)

    @handle_errors
    async def ingest_bulk(self, data: IngestRequest, chunksize: int = 32):
        total_chunks = len(data.texts) // chunksize + (len(data.texts) % chunksize > 0)

        for chunk in tqdm(
            chunker(data.texts, chunksize),
            total=total_chunks,
            desc="Ingesting",
            unit="chunks",
        ):
            await self.upsert_vectors(
                UpsertRequest(
                    vectors=[
                        UpsertVector(
                            values=await self.create_embeddings(text),
                            metadata={"text": text},
                        )
                        for text in chunk
                    ],
                    namespace=data.namespace,
                )
            )


def chunker(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


async def parse_openai_response(  # pylint: disable=dangerous-default-value
    response: dict,
    functions: List[
        Type[F]
    ] = FunctionType._subclasses,  # pylint: disable=protected-access
) -> Any:
    """Parse the response from OpenAI and return the result."""
    choice = response["choices"][0]["message"]
    if "function_call" in choice:
        function_call_ = choice["function_call"]
        name = function_call_["name"]
        arguments = function_call_["arguments"]
        for i in functions:
            if i.__name__ == name:
                result = await i.run(i(**json.loads(arguments)))
                break
        else:
            raise ValueError(f"Function {name} not found")
        return result
    return choice["content"]


async def function_call(  # pylint: disable=dangerous-default-value
    text: str,
    context: Optional[str] = None,
    model: Model = "gpt-4-0613",
    functions: List[
        Type[F]
    ] = FunctionType._subclasses,  # pylint: disable=protected-access
) -> Any:
    """
    Function to call a OpenAI function with given text and context.

    Arguments:
    text -- Input text for the function
    context -- Optional context for the function
    model -- Model to be used. Defaults to "gpt-4-0613"
    functions -- List of function types. Defaults to all subclasses of FunctionType.
    """
    if context is None:
        messages = [Message(role="user", content=text)]
    else:
        messages = [
            Message(role="system", content=context),
            Message(role="user", content=text),
        ]
    data = FunctionRequest(
        model=model, messages=messages, functions=[i.openaischema for i in functions]
    ).dict()
    response = await openai.ChatCompletion.acreate(**data)
    assert isinstance(response, dict)
    return await parse_openai_response(response, functions=functions)

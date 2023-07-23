import json
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union
from uuid import uuid4

from dotenv import load_dotenv
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module
from typing_extensions import ParamSpec

from aiofauna import *
from aiofauna.client import APIConfig
from aiofauna.logging import setup_logging

load_dotenv()

make_client = lambda base_url, headers: ApiClient(APIConfig(base_url=base_url, headers=headers))

google = make_client(base_url="https://www.google.com", headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"})



logger = setup_logging(__name__)

load_dotenv()

P = ParamSpec("P")

def make_client(base_url: str, headers: Dict[str, str]):
    return ApiClient(APIConfig(base_url=base_url, headers=headers))

pinecone = make_client(base_url=os.environ["PINECONE_BASE_URL"], headers={"api-key": os.environ["PINECONE_API_KEY"]})
openai = make_client(base_url=os.environ["OPENAI_BASE_URL"], headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"})




Vector = List[float]
MetaData = Dict[str, str]

class UpsertVector(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    values:Vector = Field(...)
    metadata: MetaData = Field(...)
    
class UpsertRequest(BaseModel):
    vectors: List[UpsertVector] = Field(..., max_items=100)
    namespace:str = Field(...)
    
class UpsertResponse(BaseModel):
    upsertedCount: int = Field(...)
    
class QueryRequest(BaseModel):
    topK: int = Field(default=4, description="The number of results to return")
    namespace: str = Field(...)
    vector: Vector = Field(...)
    includeMetadata: bool = Field(default=True, description="Whether to include metadata in the response")
    
class QueryMatch(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    score: float = Field(...)
    values: Vector = Field(...)
    metadata: MetaData = Field(...)
    
class QueryResponse(BaseModel):
    matches: List[QueryMatch] = Field(...)
    namespace: str = Field(...)

class CreateEmbeddingRequest(BaseModel):
    model: str = Field(default="text-embedding-ada-002", description="The model to use for embedding")
    input: Union[str, List[str], List[int], List[List[int]]] = Field(..., description="Input text to embed")
  
class EmbeddingData(BaseModel):
    index: int = Field(...)
    object: str = Field(...)
    embedding: List[float] = Field(...)

class Usage(BaseModel):
    prompt_tokens: int = Field(...)
    total_tokens: int = Field(...)

class CreateEmbeddingResponse(BaseModel):
    object: str = Field(...)
    model: str = Field(...)
    data: List[EmbeddingData] = Field(...)
    usage: Usage = Field(...)    


class ChatCompletionRequestMessage(BaseModel):
    role: str = Field(..., description="The role of the messages author.")
    content: Optional[str] = Field(default=None, description="The contents of the message.")
   

class ChatCompletionResponseMessage(BaseModel):
    index: int = Field(...)
    message: ChatCompletionRequestMessage = Field(...)
    finish_reason: str = Field(...)

class CreateChatCompletionRequest(BaseModel):
    model: str = Field(default="gpt-4-0613")
    messages: List[ChatCompletionRequestMessage] = Field(default_factory=list)
    temperature: float = Field(default=0.2)
    top_p: float = Field(default=1.0)
    n: int = Field(default=1)
    stream: bool = Field(default=False)
    stop: Optional[Union[str, List[str]]] = Field(default=None)
    max_tokens: int = Field(default=512)
    presence_penalty: float = Field(default=0.0)
    frequency_penalty: float = Field(default=0.0)
    logit_bias: Optional[dict] = Field(default=None)
   
class CreateChatCompletionResponse(BaseModel):
    id: str = Field(...)
    object: str = Field(...)
    created: int = Field(...)
    model: str = Field(...)
    choices: List[ChatCompletionResponseMessage] = Field(...)
    usage: Usage = Field(...)


async def upsert_vectors(request: UpsertRequest) -> UpsertResponse:
    try:
        response = await pinecone.fetch("/vectors/upsert", method="POST", json=request.dict(exclude_none=True))
        logger.info(response)
        return UpsertResponse(**response)
    except HTTPException as e:
        logger.error(e.__class__.__name__)
        logger.error(e.reason)
        raise e
    except Exception as e:
        logger.error(e.__class__.__name__)
        logger.error(str(e))
        raise e
    
async def query_vectors(request: QueryRequest) -> QueryResponse:
    try:
        response = await pinecone.fetch("/query", method="POST", json=request.dict(exclude_none=True))
        logger.info(response)
        return QueryResponse(**response)
    except HTTPException as e:
        logger.error(e.__class__.__name__)
        logger.error(e.reason)
        raise e
    except Exception as e:
        logger.error(e.__class__.__name__)
        logger.error(str(e))
        raise e
    

async def create_embedding(request: CreateEmbeddingRequest) -> CreateEmbeddingResponse:
    try:
        response = await openai.fetch("/v1/embeddings", method="POST", json=request.dict(exclude_none=True))
        logger.info(response)
        return CreateEmbeddingResponse(**response)
    except HTTPException as e:
        logger.error(e.__class__.__name__)
        logger.error(e.reason)
        raise e
    except Exception as e:
        logger.error(e.__class__.__name__)
        logger.error(str(e))
        raise e
    
async def create_chat_completion(request: CreateChatCompletionRequest) -> CreateChatCompletionResponse:
    try:
        response = await openai.fetch("/v1/chat/completions", method="POST", json=request.dict(exclude_none=True))
        logger.info(response)
        return CreateChatCompletionResponse(**response)
    except HTTPException as e:
        logger.error(e.__class__.__name__)
        logger.error(e.reason)
        raise e
    except Exception as e:
        logger.error(e.__class__.__name__)
        logger.error(str(e))
        raise e
    
async def pipeline(prompt: str, namespace: str):
    try:
        embedding_request = CreateEmbeddingRequest(input=prompt)
        embedding_response = await create_embedding(embedding_request)
        logger.info("Embedding created")
        query_request = QueryRequest(topK=5, namespace=namespace, vector=embedding_response.data[0].embedding)
        query_response = await query_vectors(query_request)
        logger.info("Querying vectors")
        system_message = ChatCompletionRequestMessage(role="system", content=query_response.matches[0].metadata["text"])
        user_message = ChatCompletionRequestMessage(role="user", content=prompt)
        chat_completion_request = CreateChatCompletionRequest(
            messages=[system_message, user_message],
        )
        logger.info("Sending chat completion request to %s", chat_completion_request.model)
        chat_completion_response = await create_chat_completion(chat_completion_request)
        embedding_request = CreateEmbeddingRequest(input=system_message.content) # type: ignore
        embedding_response = await create_embedding(embedding_request)
        text = chat_completion_response.choices[0].message.content
        assert isinstance(text, str)
        logger.info("Chat completion response: %s", text)
        upsert_request = UpsertRequest(
            vectors=[
                UpsertVector(values=embedding_response.data[0].embedding, metadata={"text": prompt}),
                UpsertVector(values=embedding_response.data[0].embedding, metadata={"text": text})
            ],
            namespace=namespace
        )
        logger.info("Upserting vectors for %s , ConversationId: %s", namespace, chat_completion_response.id)
        await upsert_vectors(upsert_request)
        return text
    except HTTPException as e:
        logger.error(e.__class__.__name__)
        logger.error(e.reason)
        raise e
    except Exception as e:
        logger.error(e.__class__.__name__)
        logger.error(str(e))
        raise e
    
class FunctionType(BaseModel, ABC):
    @classmethod    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        schema = cls.schema()
        name = cls.__name__
        description = cls.__doc__
        if not description:
            raise ValueError(f"{name} must have a docstring")
        cls.openaischema = {
            "name": cls.__name__,
            "description":cls.__doc__,
            "parameters": {
                "type": "object",
                "properties": schema["properties"],
                "required": schema["required"]
            },
        }
        
    @classmethod
    @abstractmethod
    async def run(cls, json_str:str):
        pass
    

    
async def function_call(text:str,functions:List[Type[FunctionType]]):
    data = {
        "model": "gpt-4-0613",
        "messages":[{
                "role": "user",
                "content": text
            }],
        "functions": [i.openaischema for i in functions]
    }
    response = await openai.fetch("/v1/chat/completions", method="POST", json=data)
    logger.info("Response: %s", response)
    call_struct = response['choices'][0]['message']['function_call']
    logger.info("Function call: %s", call_struct)
    name = call_struct['name']
    logger.info("Function name: %s", name)
    arguments = call_struct['arguments']
    logger.info("Function arguments: %s", arguments)
    for i in functions:
        if i.__name__ == name:
            result = await i.run(arguments)
            logger.info("Function result: %s", result)
            break
    else:
        raise ValueError(f"Function {name} not found")
    return result


async def chain_of_thoughts(initial_prompt:str,namespace:str, iterations:int=8):
    prompt = initial_prompt
    thoughts = []
    for i in range(iterations):
        logger.info("Iteration: %s", i)
        logger.info("Prompt: %s", prompt)
        prompt = await pipeline(prompt, namespace)
        logger.info("Response: %s", prompt)  
        thoughts.append(zip([i for i in range(len(prompt.split("\n")))], prompt.split("\n")))
    return thoughts




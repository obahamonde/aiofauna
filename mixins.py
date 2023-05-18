"""API Components"""
import asyncio

import botocore
from aioboto3 import Session
from aiohttp_sse import EventSourceResponse, sse_response
from dotenv import load_dotenv
from multidict import MultiDict
from pydantic import BaseConfig  # pylint: disable=no-name-in-module
from pydantic import BaseSettings, Field

from aiofauna import Api, HTTPClient, Request
from aiofauna.api import FileField
from models import *

load_dotenv()

# Settings

class Env(BaseSettings):
    """Environment Variables"""
    class Config(BaseConfig):
        env_file = ".env"
        env_file_encoding = "utf-8"
    FAUNA_SECRET:str=Field(..., env="FAUNA_SECRET")
    AUTH0_DOMAIN:str=Field(..., env="AUTH0_DOMAIN")
    AWS_ACCESS_KEY_ID:str=Field(..., env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY:str=Field(..., env="AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET:str=Field(..., env="AWS_S3_BUCKET")
    AWS_S3_ENDPOINT:str=Field(..., env="AWS_S3_ENDPOINT")
    REDIS_PASSWORD:str=Field(..., env="REDIS_PASSWORD")
    REDIS_HOST:str=Field(..., env="REDIS_HOST")
    REDIS_PORT:int=Field(..., env="REDIS_PORT")



# Singletons

session = Session() # boto3 session

client = HTTPClient() # http client
        
env = Env() # environment variables

app = Api() # application instance

state:D[str,L[EventSourceResponse]]=MultiDict() # state

# Mixins

@app.get("/api/sse")
async def sse_handler(request:Request)->EventSourceResponse:
    async with sse_response(request) as resp:
        await resp.prepare(request)
        params = dict(request.query)
        if "ref" not in params:
            raise Exception("Missing ref")
        ref = params["ref"]
        if ref in state:
            state[ref].append(resp)
        else:
            state[ref] = [resp]
        while True:
            await asyncio.sleep(1)
    return resp

@app.post("/api/messages")
async def post_message(msg:Message):
    message = await msg.create()
    assert isinstance(message, Message)
    tasks = []
    for k, v in state.items():
        if k == message.conversation:
            tasks.extend([v_.send(message.json()) for v_ in v]) 
    await asyncio.gather(*tasks)
    conversation = await Conversation.get(message.conversation)
    assert isinstance(conversation, Conversation)
    conversation.messages.append(message.dict())
    instance = await conversation.save()
    assert isinstance(instance.ref, str)
    response = await fetch_conversation_details(instance.ref)
    return response

@app.post("/api/upload")
async def upload_handler(request:Request):
    """
    Upload Endpoint
    """
    data = await request.post()
    params = dict(request.query)
    key = params.get("key")
    size = params.get("size")
    user = params.get("user")
    if key and size and user:
        size = int(size)
        file = data["file"]
        if isinstance(file, FileField):
            async with session.client(service_name="s3", 
            aws_access_key_id=env.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY,
            endpoint_url=env.AWS_S3_ENDPOINT,
            config=botocore.config.Config(signature_version="s3v4")) as s3client: # type: ignore
                key_ = f"{key}/{file.filename}" # type: ignore
                await s3client.put_object(Bucket=env.AWS_S3_BUCKET, Key=key_, Body=file.file.read(), ContentType=file.content_type, ACL="public-read")
                url = await s3client.generate_presigned_url("get_object", Params={"Bucket": env.AWS_S3_BUCKET, "Key": key_}, ExpiresIn=3600*7*24)
                return await Upload(user=user,key=key_, name=file.filename, size=size, type=file.content_type, url=url).save()     
    return {"message": "Invalid request", "status": "error"}

async def fetch_conversation_details(conversation_id: str):
    '''Fetches all messages for a conversation'''
    conversation = await Conversation.get(conversation_id)
    assert isinstance(conversation, Conversation)
    assert isinstance(conversation.messages, list)
    owner = await User.get(conversation.owner)
    assert isinstance(owner, User)
    guest = await User.get(conversation.guest)
    assert isinstance(guest, User)
    return {
        "ref": conversation.ref,
        "ts": conversation.ts,
        "name": conversation.name,
        "owner": owner.dict(),
        "guest": guest.dict(),
        "messages": [m.dict() for m in conversation.messages]
    }

@app.get("/api/conversations/{user_id}")
async def fetch_user_conversations(user_id: str):
    '''Fetches all conversations for a user'''
    results = []
    user = await User.get(user_id)
    assert isinstance(user, User)
    instances = await Conversation.find_many("owner", user_id) + await Conversation.find_many("guest", user_id)
    if len(instances) == 0:
        instances.append(await Conversation(
            owner=user_id,  
            guest=user_id
        ).save())
    for instance in instances:
        assert isinstance(instance, Conversation)
        assert isinstance(instance.ref, str)
        results.append(fetch_conversation_details(instance.ref))
    return await asyncio.gather(*results)

@app.get("/api/new_conversation/{user_id}")
async def create_new_conversation(user_id: str, contact: str):
    '''Creates a new conversation'''
    user = await User.get(user_id)
    owner = await User.get(contact)
    assert isinstance(user, User)
    assert isinstance(owner, User)
    instance = await Conversation(owner=user_id, guest=contact).save()
    assert isinstance(instance, Conversation)
    assert isinstance(instance.ref, str)
    return await fetch_conversation_details(instance.ref)
    
@app.post("/api/conversations/{conversation_id}")
async def post_message_to_conversation(conversation_id: str, msg: Message):
    '''Posts a message to a conversation'''
    message = await msg.save()
    assert isinstance(message, Message)
    instance = await Conversation.get(conversation_id)
    assert isinstance(instance, Conversation)
    assert isinstance(instance.messages, list)
    instance.messages.append(message)
    instance = await instance.save()
    assert isinstance(instance, Conversation)
    assert isinstance(instance.ref, str)
    return await fetch_conversation_details(instance.ref)

@app.get("/api/online/{user_id}")
async def is_user_online(user_id: str):
    '''Checks if a user is online'''
    for k, v in state.items():
        instance = await Conversation.get(k)
        assert isinstance(instance, Conversation)
        if user_id in (instance.owner, instance.guest):
            return {"online": True}
    return {"online": False}


@app.get("/api/messages/{conversation_id}")
async def fetch_messages(conversation_id: str):
    '''Fetches all messages for a conversation'''
    messages = await Message.find_many("conversation", conversation_id)
    assert isinstance(messages, list)
    return [m.dict() for m in messages]

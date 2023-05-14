import json
from typing import Dict, List
from pydantic import BaseModel, BaseConfig, BaseSettings, Field
from aiohttp_sse import EventSourceResponse, sse_response
from models import *
import asyncio
from aiofauna import Request, Response, Api, HTTPClient
from aioboto3 import Session
from dotenv import load_dotenv
from aiofauna.api import UploadFile, FileField
load_dotenv()

# Settings1

class Env(BaseSettings):
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
    
    
    def __init__(self):
        super().__init__()

# Singletons

session = Session()

client = HTTPClient()
        
env = Env()

app = Api()

state = {}

# Mixins

@app.get("/api/messages")
async def sse_handler(request:Request)->EventSourceResponse:
    async with sse_response(request) as resp:
        await resp.prepare(request)
        params = dict(request.query)
        if "ref" not in params:
            raise Exception("Missing ref")
        ref = params["ref"]
        state[ref] = resp
        while True:
            await asyncio.sleep(1)

@app.post("/api/messages")
async def post_message(message:str):
    for ref, resp in state.items():
        await resp.send(message)
    return "OK"

@app.post("/api/upload")
async def upload_endpoint(request: Request):
    params = dict(request.query)
    if "ref" not in params:
        raise Exception("Missing ref") # pylint: disable=all
    ref = params["ref"]
    data = await request.post()
    file = data["file"]
    assert isinstance(file, FileField)
    _bytes = file.file.read()
    upload_file = UploadFile(filename=file.filename, content_type=file.content_type,data= _bytes, size=len(_bytes),headers=dict(request.headers)) 
    key = file.filename
    async with session.client(service_name="s3", region_name="us-east-1",aws_access_key_id=env.AWS_ACCESS_KEY_ID,aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY,endpoint_url=env.AWS_S3_ENDPOINT) as client:
        await client.put_object(Bucket=env.AWS_S3_BUCKET, Key=file.filename, Body=upload_file.data, ContentType=upload_file.content_type)
        url = await client.generate_presigned_url('get_object', Params={'Bucket': env.AWS_S3_BUCKET, 'Key': key}, ExpiresIn=3600)   
        return await UserUpload(user=ref, file=upload_file, url=url).save()
        

    
        
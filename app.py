import math
import os
from functools import wraps
from json import dumps, loads
from pathlib import Path
from typing import *

import openai
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, AgentType, Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import (AIMessagePromptTemplate,
                               HumanMessagePromptTemplate,
                               SystemMessagePromptTemplate)
from langchain.schema import AIMessage, HumanMessage, SystemMessage

load_dotenv()

T = TypeVar("T")  

Role = Literal["user","assistant","system"]


def tree_to_json(path:str=".")->dict:
    path_ = Path(path)
    if not path_.exists():
        raise FileNotFoundError(f"{path} does not exist")
    if path_.is_file():
        try:
            return path_.read_text()
        except:
            return "[binary]"
    else:
        return {i.name:tree_to_json(i) for i in path_.iterdir()}
    
    
def get_tree(path:str=".")->str:
    path_ = Path(path)
    if not path_.exists():
        raise FileNotFoundError(f"{path} does not exist")
    if path_.is_file():
        try:
            return path_.read_text()
        except:
            return "[binary]"
    else:
        dct = {i.name:tree_to_json(i) for i in path_.iterdir()}
        for k, v in dct.items():
            if isinstance(v, dict):
                text = f"{k}\n" + "\n".join([f"├── {i}" for i in v.keys()])
            else:
                text = f"{k}\n" + "\n".join([f"├── {i}" for i in v.split("\n")])        
            dct[k] = text
        return "\n".join([f"├── {i}" for i in dct.keys()]) + "\n" + "\n".join(dct.values())

def token_estimate(text:str):
    byte_size = len(text.encode('utf-8'))
    return math.ceil(byte_size / 4)


def divide_in_chunks_for_openai_api(text:str, max_tokens:int=1024):
    tokens = token_estimate(text)
    if tokens <= max_tokens:
        yield text
    else:
        for i in range(math.ceil(tokens / max_tokens)):
            yield text[i*max_tokens:(i+1)*max_tokens]
            


PINECONE_API_KEY=os.environ["PINECONE_API_KEY"]
PINECONE_INDEX=os.environ["PINECONE_INDEX"]
PINECONE_ENVIRONMENT=os.environ["PINECONE_ENVIRONMENT"]

import pinecone as pc
from langchain.vectorstores import Pinecone

pc.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)                                         

pinecone = Pinecone.from_texts(texts = [], embedding=OpenAIEmbeddings(), index_name=PINECONE_INDEX) # type: ignore

llm = ChatOpenAI() # type: ignore


test_code_prompt_template = SystemMessagePromptTemplate.from_template(
    """
    You are a QA Tester. You are testing a new program, and you are tasked with writing a test case for the following code:
    """
)

run_code_prompt_template = SystemMessagePromptTemplate.from_template(
    """
    You are a QA Tester. You are testing a new program, and you are tasked with running the following code and reporting any bugs:
    """
)

from langchain.tools import PythonAstREPLTool, PythonREPLTool, ShellTool

tools = [PythonREPLTool, PythonAstREPLTool, ShellTool]

agent = initialize_agent(tools=tools,llm=llm,agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True)

for chunk in get_tree():
    agent.run(chunk)
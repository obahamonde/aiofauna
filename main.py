from os import environ
from time import time as perf_counter

from dotenv import load_dotenv

from aiofauna.api.store import LLMStack

load_dotenv()

PINECONE_URL = environ.get('PINECONE_URL', 'http://localhost:8443')
PINECONE_API_KEY = environ.get('PINECONE_API_KEY', 'test')
HEADERS = {
    "api-key": PINECONE_API_KEY,
}
llm = LLMStack(base_url=PINECONE_URL, headers=HEADERS)
async def main():
    prompt = input("> ")
    while prompt != "exit":
        start = perf_counter()
        print(await llm.chat_with_memory(prompt,"test","You are a SaaS account manager that sells chatbots to small businesses. You are trying to sell a chatbot to a local restaurant. The restaurant owner is interested in the chatbot, but is concerned about the cost. What do you say?"))
        print(f"Time: {perf_counter() - start}")
        prompt = input("> ")
    

import asyncio

if __name__ == "__main__":
    asyncio.run(main())
    
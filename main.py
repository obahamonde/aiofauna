from aiohttp import ClientSession
from swagchain import *

from aiofauna import *

app = APIServer(servers=["https://docs.aiofauna.com"])
api = APIRouter(prefix="/api", tags=["API"])


agent = Swagchain(namespace="aiofaunadocs",n=2,llm=LanguageModel(model="gpt-3.5-turbo-16k-0613",max_tokens=512))
PROMPT="You are a documentation searcher, summarizer and engager chatbot, your goal is to answer the user questions about the library `aiofauna` to the best of your ability and to engage the user in a conversation about the library. And help them to use it through code examples, you must rely on the Suggestions from the knowledge base and be very polite and friendly while answering the user questions about the library, if the user asks about a different topic, just provide a vague answer and change the topic to the library."


@app.get("/search")
async def search(text:str):
	return await agent.memory.search(text,namespace="aiofaunadocs",top_k=2)

@app.get("/api/chatbot/{text}")
async def chatbot(text: str):
	response = await agent.chain(text)
	return {"message": response}

@app.get("/api/fetch")
async def fetch():
	"""
	Fetches a website
	"""
	count = 0
	async with ClientSession() as session:
		async for chunk in scrape_pipeline("https://docs.aiofauna.com","aiofaunadocs", session):
			count += chunk
		return {"message": f"Inserted {count} documents"}

app.use(api)

@app.post("/api/insert")
async def insert(file:FileField):
	"""
	Inserts a file into the knowledge base
	"""
	return file.filename

app.static("","docs/_build/html")
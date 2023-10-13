from swagchain import *

from aiofauna import *

app = APIServer(servers=["https://docs.aiofauna.com"])
api = APIRouter(prefix="/api", tags=["API"])
agent = Swagchain(namespace="aiofaunadocs",n=3,llm=LanguageModel(model="gpt-3.5-turbo-16k-0613",max_tokens=1024))
@api.get("/chatbot/{text}")
async def chatbot(text: str):
	response = await agent.chain(text)
	return {"message": response}
app.use(api)
app.static("","docs/_build/html")
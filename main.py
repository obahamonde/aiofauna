import asyncio
from aiofauna import FaunaClient, APIServer, EventSourceResponse, to_json,q

app = APIServer()
fauna = FaunaClient()

@app.sse("/stream")
async def stream(sse: EventSourceResponse):
	while True:
		now = await fauna.query(q.now())
		await sse.send(to_json(now["@ts"]))
		await asyncio.sleep(1)
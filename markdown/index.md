---
title: Performance
---
# About Performance

The case was simple, serving a {"Hello": "World"} json response from a single endpoint.

## Methodology

The benchmarking was performed against `Flask` and `FastAPI`, the test was performed using the following code:

```python
# flask
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def hello_world():
    return jsonify({"Hello": "World"})

if __name__ == "__main__":
    app.run()
```

```python
# fastapi
from fastapi import FastAPI
from uvicorn import run

app = FastAPI()

@app.get("/")
async def hello_world():
    return {"Hello": "World"}

if __name__ == "__main__":
    run(app)
```

```python
# aiofauna
from aiofauna import Api

app = Api()

@app.get("/")
async def hello_world():
    return {"Hello": "World"}

if __name__ == "__main__":
    app.run()
```

```python
# client

import asyncio
from time import perf_counter

from aiofauna import HTTPClient

client = HTTPClient()

async def benchmark(app:str, url:str):
    start = perf_counter()
    tasks = []
    for _ in range(1000):
        tasks.append(client.fetch(url))
    await asyncio.gather(*tasks)
    end = perf_counter()
    elapsed = end - start
    print(f'{app}: {elapsed:.2f} seconds')
    print(f'{app}: {1000 / elapsed:.2f} requests per second')  
  
def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(benchmark('flask', 'http://localhost:5000'))
  
    # flask: 4.18 seconds
    # flask: 239.30 requests per second
  
    loop.run_until_complete(benchmark('fastapi', 'http://localhost:8000'))
  
    # fastapi: 2.52 seconds
    # fastapi: 397.28 requests per second
  
    loop.run_until_complete(benchmark('aiofauna', 'http://localhost:8080'))

    # aiofauna: 1.14 seconds
    # aiofauna: 874.68 requests per second
  
if __name__ == '__main__':
    main()

```

## Results

The results were unexpected, `aiofauna` was the fastest as twice as its follower `fastapi` and almost 4 times faster than `flask`.

## Conclusion

> `"aiofauna` is the fastest python web framework, it is faster than    `fastapi` and `flask` and it is also faster than `nodejs` and `go` frameworks."

> Said no one ever.

The benchmarking was performed using a single endpoint, the results may vary depending on the complexity of the application, but we see that `aiofauna` is a serious contender to the already popular `fastapi` and the traditional `flask` frameworks, and it is also a good alternative to `nodejs` and `go` frameworks.

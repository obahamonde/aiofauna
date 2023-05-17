import asyncio
import functools as ft
import typing as t

from aiohttp.web_ws import WebSocketReady, WebSocketResponse, WSMsgType

from aiofauna import Api, Request, Response


class WebSocket(Api):
    def websocket(self, path: str) -> t.Callable:
        def decorator(func: t.Callable) -> t.Callable:
            @ft.wraps(func)
            async def wrapper(request: Request) -> WebSocketResponse:
                wsocket = WebSocketResponse()
                await wsocket.prepare(request)
                if asyncio.iscoroutinefunction(func):
                    await func(request, wsocket)
                else:
                    func(request, wsocket)
                return wsocket
            self.router.add_get(path, wrapper)
            return wrapper
        return decorator
    
    
app = WebSocket()

html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>WebSocket demo</title>
</head>
<body>
    <div id="messages"></div>
    <script>
        var ws = new WebSocket("ws://localhost:5000/ws");
        ws.onmessage = function(event) {
            var messages = document.getElementById('messages');
            var message = document.createElement('div');
            var content = document.createTextNode(event.data);
            message.appendChild(content);
            messages.appendChild(message);
        };
    </script>
</body>
</html>
"""

app = WebSocket()

@app.websocket('/ws')
async def websocket_handler(req:Request, ws:WebSocketResponse):
    await ws.send_str("Hello, world!")
    await ws.close()

@app.get("/")
async def index():
    return Response(text=html, content_type="text/html")
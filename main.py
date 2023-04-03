from aiofauna import *
import os

from dotenv import load_dotenv

load_dotenv()

class env:
    FAUNA_SECRET = os.environ["FAUNA_SECRET"]

html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Server-Sent Events</title>
</head>
<body>
   <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.20.1/moment.js"></script>
   <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.1/Chart.js"></script>
   <div class="container main">

  <div style="height: 300px">
    <canvas id="canvas-foobar"></canvas>
  </div>

</div>
<script>
    var ctx = document.getElementById("canvas-foobar").getContext("2d");
    var myChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: "Latency",
                data: [],
                backgroundColor: "rgba(0, 99, 132, 0.2)",
                borderColor: "rgba(0,99,132,1)",
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:false
                    }
                }]
            }
        }
    });
    
    var source = new EventSource("/sse");
    source.onmessage = function(event) {
        var faunaTime = moment(event.data);
        var now = moment();
        var latency = now.diff(faunaTime, "milliseconds");
        myChart.data.labels.push(faunaTime.format("HH:mm:ss"));
        myChart.data.datasets[0].data.push(latency);
        myChart.update();
    };
    
    while (myChart.data.labels.length > 100){
        myChart.data.labels.shift();
        myChart.data.datasets[0].data.shift();
    }
</script>   
</body>
</html>
"""


async def index_handler(request: Request) -> Response:
    """Index handler."""

    print(request)

    return Response(body=html, content_type="text/html", charset="utf-8",)


async def sse_handler(request: Request) -> Response:
    """SSE handler."""
    async with sse_response(request) as resp:
        while True:
            _ = (await Client(env.FAUNA_SECRET).query(q.now()))["@ts"] # type: ignore
            await resp.send(f"{_}")
            await asyncio.sleep(1)
            
async def create_app():

    """Create application."""

    app = Application()

    # Add routes

    app.router.add_get("/", index_handler)

    app.router.add_get("/sse", sse_handler)

    runner = AppRunner(app)
    await runner.setup()
    site = TCPSite(runner, "localhost", 8000)
    await site.start()
    await asyncio.sleep(1000)

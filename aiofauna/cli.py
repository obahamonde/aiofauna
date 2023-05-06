"""AIOFauna CLI."""
import click
from asyncio import get_event_loop, AbstractEventLoop
from aiohttp_devtools.cli import cli, runserver
from pydantic import main
from watchgod import awatch

async def watch_changes(loop:AbstractEventLoop,path:str):
    async for changeset in awatch(path):
        for change in changeset:
            status, path = change
            print(f"File {path} has been {status._name_}")

@cli.command()            
@click.option()
def dev():
    """
    Run the development server.
    """
    print(f"https://localhost:8000")
    loop = get_event_loop()
    while True:
        try:
            runserver()
            loop.run_until_complete(watch_changes(loop,"./"))
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)
            break
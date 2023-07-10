import asyncio
import logging
from typing import Optional, cast

from aiohttp.web import Application, AppRunner, TCPSite
from rich.console import Console
from rich.logging import RichHandler
from watchdog.events import (FileCreatedEvent, FileDeletedEvent,
                             FileModifiedEvent, FileSystemEventHandler)
from watchdog.observers import Observer

from .api import Api

console = Console(record=True)

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, loop, task, logger):
        self.loop = loop
        self.task = task
        self.logger = logger

    def on_modified(self, event):
        self.logger.info(f"File modified: {event.src_path}")
        self.loop.call_soon_threadsafe(self.task.cancel)

    def on_created(self, event):
        self.logger.info(f"File created: {event.src_path}")
        self.loop.call_soon_threadsafe(self.task.cancel)

    def on_deleted(self, event):
        self.logger.info(f"File deleted: {event.src_path}")
        self.loop.call_soon_threadsafe(self.task.cancel)
            

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
        force=True,
    )

    logger = logging.getLogger("rich")
    logger.setLevel(logging.INFO)
    return logger


class AioFauna(Api):
    """AioFauna CLI"""

    runner: Optional[AppRunner] = None
    site: Optional[TCPSite] = None
    file_watcher: Optional[asyncio.Task] = None
    host: str = "localhost"
    port: int = 8080

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = setup_logging()

    async def run_(self):
        self.runner = AppRunner(cast(Application, self))
        self.logger.info("Starting server...")
        await self.runner.setup()
        self.site = TCPSite(self.runner, self.host, self.port)
        await self.site.start()
        self.logger.info("Server running on http://%s:%s", self.host, self.port)

    def run(self):
        loop = asyncio.get_event_loop()
        while True:
            task = asyncio.ensure_future(self.run_(), loop=loop)
            observer = Observer()
            observer.schedule(ReloadHandler(loop, task, self.logger), '.', recursive=True)
            observer.start()

            try:
                loop.run_forever()
            except KeyboardInterrupt:
                observer.stop()
                observer.join()
                self.logger.info("Stopping server...")
                break
            except Exception as e:
                observer.stop()
                observer.join()
                self.logger.error(e)
                break
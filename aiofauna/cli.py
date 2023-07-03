import asyncio
import importlib
import logging
import os
import sys
from typing import Optional

import click
from aiohttp.web import AppRunner, TCPSite
from rich.console import Console
from rich.logging import RichHandler

from .api import Api

console = Console(record=True)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
        force=True
    )

    logger = logging.getLogger("rich")
    logger.setLevel(logging.INFO)
    return logger

class AioFauna(Api):
    """AioFauna CLI"""
    runner: Optional[AppRunner] = None
    site: Optional[TCPSite] = None
    file_watcher: Optional[asyncio.Task] = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = setup_logging()
    
    async def run(self, host:str, port:int)->None:
        self.runner = AppRunner(self)
        await self.runner.setup()
        self.site = TCPSite(self.runner, host, port)
        await self.site.start()
        self.logger.info("Server running on http://%s:%s", host, port)        
    
    async def dev(self, host: str, port: int):
        """Runs the server in development mode"""
        try:
            self.logger.info("Running in debug mode")
            await self.run(host, port)
            self.file_watcher = asyncio.create_task(self._setup_watchers())
        except KeyboardInterrupt:   
            self.logger.info("Stopping server...")
            await self.stop()
            self.logger.info("Server stopped")    
        
    async def stop(self):
        self.logger.info("Stopping server...")
        await self.runner.cleanup() # type: ignore
        self.file_watcher.cancel() # type: ignore
        self.logger.info("Server stopped")
        
    async def _setup_watchers(self):
        path_to_watch =os.getcwd()
        file_mod_times = self.track_files(path_to_watch)
        
        while True:
            new_mod_times = self.track_files(path_to_watch)
            if new_mod_times != file_mod_times:
                self.logger.info("Restarting server...")
                await self.stop()
                os.execv(sys.executable, ["python"] + sys.argv)
                
    @staticmethod
    def track_files(path_to_watch):
        file_mod_times = {}
        for dirpath, _, filenames in os.walk(path_to_watch):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                file_mod_times[path] = os.path.getmtime(path)
        return file_mod_times
    
    
@click.command()
@click.option("--module", default="main", help="Python module that contains the application")
@click.option("--host", default="0.0.0.0", help="Host to run the server on")
@click.option("--port", default=8080, help="Port to run the server on")
def dev(module, host: str, port: int):
    """Runs the server in development mode"""
    try:
        module = importlib.import_module(module)
    except ImportError:
        try:
            module = importlib.import_module('main')
        except ImportError:
            raise ImportError("Could not find an application to run. Please specify a Python module that contains your application using the --module option.")
    app = getattr(module, 'app', None)
    if app is None:
        raise ValueError(f"The module '{module.__name__}' does not contain a variable named 'app'.")

    async def run_dev_and_handle_keyboard_interrupt():
        try:
            await app.dev(host, port)
        except KeyboardInterrupt:
            await app.stop()

    asyncio.run(run_dev_and_handle_keyboard_interrupt())
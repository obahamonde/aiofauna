import logging
import os
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler
from rich.pretty import install
from rich.traceback import install as ins


def setup_logging(name) -> logging.Logger:
    """Set's up logging"""
    
    install()
    ins()
    
    console = Console(record=True, force_terminal=True)
    
    path = Path(os.getcwd()) / "logs"
    path.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(
        filename=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
        mode="w",
        encoding="utf-8",
    )
    file_handler.setFormatter(logging.Formatter("%(message)s"))
    file_handler.setLevel(logging.INFO)
    console_handler = RichHandler(
        console=console,
        show_time=True,
        show_path=True,
        markup=True,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        tracebacks_extra_lines=5,
        tracebacks_theme="solarized",
    )
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    console_handler.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    return logger

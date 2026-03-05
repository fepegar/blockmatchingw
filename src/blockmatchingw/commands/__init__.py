"""Shared helpers for CLI commands."""

import sys

import typer
from loguru import logger

from blockmatchingw.enums import LogLevel
from blockmatchingw.wrapper import run


def setup_logger(log_level: LogLevel) -> None:
    """Configure loguru for CLI output."""
    logger.configure(extra={"executable": "blockmatchingw"})
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{extra[executable]}</level> | <level>{level: <8}</level> | <level>{message}</level>",
        level=log_level.value,
        colorize=True,
    )


def make_help_callback(tool: str):
    """Create an eager Typer callback that shows the original binary help."""

    def _callback(value: bool) -> None:
        if value:
            run(tool, "-h")
            raise typer.Exit()

    return _callback

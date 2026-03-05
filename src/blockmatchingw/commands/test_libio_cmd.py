"""CLI command for test-libio."""

from pathlib import Path
from typing import Annotated

import typer
from loguru import logger

from blockmatchingw.commands import make_help_callback, setup_logger
from blockmatchingw.enums import LogLevel
from blockmatchingw.wrapper import run

_help_callback = make_help_callback("test-libio")


def test_libio(
    files: Annotated[
        list[Path],
        typer.Argument(help="Files to test I/O with."),
    ],
    _: Annotated[
        bool,
        typer.Option(
            "--print-help",
            "-h",
            is_eager=True,
            callback=_help_callback,
            help="Print the original test-libio help and exit.",
        ),
    ] = False,
    log_level: Annotated[
        LogLevel,
        typer.Option(
            "--log",
            case_sensitive=False,
            help="Set the log level.",
            rich_help_panel="Logging",
        ),
    ] = LogLevel.DEBUG,
) -> None:
    """Test I/O library."""
    setup_logger(log_level)
    tool_logger = logger.bind(executable="test-libio")

    args: list[str] = [str(f) for f in files]
    run("test-libio", *args, tool_logger=tool_logger)

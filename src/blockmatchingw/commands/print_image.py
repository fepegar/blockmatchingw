"""CLI command for printImage."""

from pathlib import Path
from typing import Annotated

import typer
from loguru import logger

from blockmatchingw.commands import make_help_callback, setup_logger
from blockmatchingw.enums import LogLevel
from blockmatchingw.wrapper import run

_help_callback = make_help_callback("printImage")


def print_image(
    images: Annotated[
        list[Path],
        typer.Argument(help="Image file(s) to print information about."),
    ],
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Enable verbose output.")
    ] = False,
    no_verbose: Annotated[
        bool, typer.Option("--no-verbose", help="Disable verbose output.")
    ] = False,
    _: Annotated[
        bool,
        typer.Option(
            "--print-help",
            "-h",
            is_eager=True,
            callback=_help_callback,
            help="Print the original printImage help and exit.",
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
    """Print image information."""
    setup_logger(log_level)
    tool_logger = logger.bind(executable="printImage")

    args: list[str] = [str(img) for img in images]
    if verbose:
        args.append("-v")
    if no_verbose:
        args.append("-nv")

    run("printImage", *args, tool_logger=tool_logger)

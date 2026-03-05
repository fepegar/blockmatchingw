"""CLI command for printTrsf."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from loguru import logger

from blockmatchingw.commands import make_help_callback, setup_logger
from blockmatchingw.enums import LogLevel
from blockmatchingw.wrapper import run

_help_callback = make_help_callback("printTrsf")


def print_trsf(
    transformations: Annotated[
        list[Path],
        typer.Argument(help="Transformation file(s) to print information about."),
    ],
    transformation_type: Annotated[
        Optional[str],
        typer.Option(
            "--transformation-type",
            help="Transformation type for interpretation.",
        ),
    ] = None,
    module: Annotated[
        Optional[Path],
        typer.Option("--module", help="Write transformation modulus to file."),
    ] = None,
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
            help="Print the original printTrsf help and exit.",
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
    """Print transformation information."""
    setup_logger(log_level)
    tool_logger = logger.bind(executable="printTrsf")

    args: list[str] = [str(t) for t in transformations]
    if transformation_type is not None:
        args.extend(["-trsf-type", transformation_type])
    if module is not None:
        args.extend(["-module", str(module)])
    if verbose:
        args.append("-v")
    if no_verbose:
        args.append("-nv")

    run("printTrsf", *args, tool_logger=tool_logger)

"""CLI command for intermediaryTrsf."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from loguru import logger

from blockmatchingw.commands import make_help_callback, setup_logger
from blockmatchingw.enums import LogLevel
from blockmatchingw.wrapper import run

_help_callback = make_help_callback("intermediaryTrsf")


def intermediary_trsf(
    input_trsf: Annotated[
        Optional[Path],
        typer.Option("--input", "-i", help="Input transformation."),
    ] = None,
    output_trsf: Annotated[
        Optional[Path],
        typer.Option("--output", "-o", help="Output transformation."),
    ] = None,
    time_point: Annotated[
        Optional[float],
        typer.Option(
            "--time-point",
            help="Intermediary time point between 0.0 and 1.0.",
        ),
    ] = None,
    time_to_1: Annotated[
        bool,
        typer.Option(
            "--time-to-1",
            help="Compute transformation from time t to time 1 (default).",
        ),
    ] = False,
    time_to_0: Annotated[
        bool,
        typer.Option(
            "--time-to-0",
            help="Compute transformation from time t to time 0.",
        ),
    ] = False,
    template: Annotated[
        Optional[Path],
        typer.Option("--template", help="Template image for vector field geometry."),
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
            help="Print the original intermediaryTrsf help and exit.",
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
    """Compute intermediary transformations."""
    setup_logger(log_level)
    tool_logger = logger.bind(executable="intermediaryTrsf")

    args: list[str] = []
    if input_trsf is not None:
        args.append(str(input_trsf))
    if output_trsf is not None:
        args.append(str(output_trsf))
    if time_point is not None:
        args.extend(["-t", str(time_point)])
    if time_to_1:
        args.append("-t-to-1")
    if time_to_0:
        args.append("-t-to-0")
    if template is not None:
        args.extend(["-template", str(template)])
    if verbose:
        args.append("-v")
    if no_verbose:
        args.append("-nv")

    run("intermediaryTrsf", *args, tool_logger=tool_logger)

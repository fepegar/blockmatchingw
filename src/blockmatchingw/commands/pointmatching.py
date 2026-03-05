"""CLI command for pointmatching."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from loguru import logger

from blockmatchingw.commands import make_help_callback, setup_logger
from blockmatchingw.enums import LogLevel
from blockmatchingw.wrapper import run

_help_callback = make_help_callback("pointmatching")


def pointmatching(
    reference: Annotated[
        Path,
        typer.Option("--reference", "-r", help="Reference image."),
    ],
    floating: Annotated[
        Path,
        typer.Option("--floating", "-f", help="Floating image."),
    ],
    result: Annotated[
        Optional[Path],
        typer.Option("--result", help="Result image."),
    ] = None,
    result_transformation: Annotated[
        Optional[Path],
        typer.Option(
            "--result-transformation",
            help="Output transformation in real coordinates.",
        ),
    ] = None,
    transformation_type: Annotated[
        Optional[str],
        typer.Option(
            "--transformation-type",
            help="Transformation type (e.g. 'rigid3D', 'affine3D').",
        ),
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
            help="Print the original pointmatching help and exit.",
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
    """Point matching-based registration."""
    setup_logger(log_level)
    tool_logger = logger.bind(executable="pointmatching")

    args: list[str] = ["-ref", str(reference), "-flo", str(floating)]
    if result is not None:
        args.extend(["-res", str(result)])
    if result_transformation is not None:
        args.extend(["-res-trsf", str(result_transformation)])
    if transformation_type is not None:
        args.extend(["-trsf-type", transformation_type])
    if verbose:
        args.append("-v")
    if no_verbose:
        args.append("-nv")

    run("pointmatching", *args, tool_logger=tool_logger)

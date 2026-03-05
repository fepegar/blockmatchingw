"""CLI command for applyTrsfToPoints."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from loguru import logger

from blockmatchingw.commands import make_help_callback, setup_logger
from blockmatchingw.enums import LogLevel
from blockmatchingw.wrapper import run

_help_callback = make_help_callback("applyTrsfToPoints")


def apply_trsf_to_points(
    input_points: Annotated[
        Path,
        typer.Option("--input", "-i", help="Input point file."),
    ],
    output_points: Annotated[
        Optional[Path],
        typer.Option("--output", "-o", help="Output point file."),
    ] = None,
    transformation: Annotated[
        Optional[Path],
        typer.Option(
            "--transformation",
            "-t",
            help="Transformation file to apply.",
        ),
    ] = None,
    voxel_transformation: Annotated[
        Optional[Path],
        typer.Option(
            "--voxel-transformation",
            help="Transformation file in voxel coordinates.",
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
            help="Print the original applyTrsfToPoints help and exit.",
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
    """Apply a transformation to point sets."""
    setup_logger(log_level)
    tool_logger = logger.bind(executable="applyTrsfToPoints")

    args: list[str] = [str(input_points)]
    if output_points is not None:
        args.append(str(output_points))
    if transformation is not None:
        args.extend(["-trsf", str(transformation)])
    if voxel_transformation is not None:
        args.extend(["-voxel-trsf", str(voxel_transformation)])
    if verbose:
        args.append("-v")
    if no_verbose:
        args.append("-nv")

    run("applyTrsfToPoints", *args, tool_logger=tool_logger)

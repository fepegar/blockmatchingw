"""CLI command for interpolateImages."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from loguru import logger

from blockmatchingw.commands import make_help_callback, setup_logger
from blockmatchingw.enums import LogLevel
from blockmatchingw.wrapper import run

_help_callback = make_help_callback("interpolateImages")


def interpolate_images(
    floating: Annotated[
        Path,
        typer.Option("--floating", "-f", help="First/left input image."),
    ],
    reference: Annotated[
        Path,
        typer.Option("--reference", "-r", help="Second/right input image."),
    ],
    result: Annotated[
        Optional[Path],
        typer.Option("--result", help="Result image (format)."),
    ] = None,
    transformation: Annotated[
        Optional[Path],
        typer.Option(
            "--transformation",
            "-t",
            help="Transformation file in real coordinates.",
        ),
    ] = None,
    voxel_transformation: Annotated[
        Optional[Path],
        typer.Option(
            "--voxel-transformation",
            help="Transformation file in voxel coordinates.",
        ),
    ] = None,
    index: Annotated[
        Optional[float],
        typer.Option(
            "--index",
            help="Interpolation position between 0 and 1.",
        ),
    ] = None,
    nimages: Annotated[
        Optional[int],
        typer.Option("--nimages", help="Number of intermediary images."),
    ] = None,
    write_extremities: Annotated[
        bool,
        typer.Option("--write-extremities", help="Interpolate at extremities."),
    ] = False,
    interpolation: Annotated[
        Optional[str],
        typer.Option(
            "--interpolation",
            help="Interpolation mode: 'nearest', 'linear', or 'cspline'.",
        ),
    ] = None,
    template: Annotated[
        Optional[Path],
        typer.Option("--template", help="Template image for output geometry."),
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
            help="Print the original interpolateImages help and exit.",
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
    """Interpolate between images."""
    setup_logger(log_level)
    tool_logger = logger.bind(executable="interpolateImages")

    args: list[str] = ["-flo", str(floating), "-ref", str(reference)]
    if result is not None:
        args.extend(["-res", str(result)])
    if transformation is not None:
        args.extend(["-trsf", str(transformation)])
    if voxel_transformation is not None:
        args.extend(["-voxel-trsf", str(voxel_transformation)])
    if index is not None:
        args.extend(["-i", str(index)])
    if nimages is not None:
        args.extend(["-n", str(nimages)])
    if write_extremities:
        args.append("-we")
    if interpolation is not None:
        args.extend(["-interpolation", interpolation])
    if template is not None:
        args.extend(["-t", str(template)])
    if verbose:
        args.append("-v")
    if no_verbose:
        args.append("-nv")

    run("interpolateImages", *args, tool_logger=tool_logger)

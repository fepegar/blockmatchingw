"""CLI command for copyTrsf."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from loguru import logger

from blockmatchingw.commands import make_help_callback, setup_logger
from blockmatchingw.enums import LogLevel
from blockmatchingw.wrapper import run

_help_callback = make_help_callback("copyTrsf")


def copy_trsf(
    input_trsf: Annotated[
        Optional[Path],
        typer.Option("--input", "-i", help="Input transformation."),
    ] = None,
    output_trsf: Annotated[
        Optional[Path],
        typer.Option("--output", "-o", help="Output transformation."),
    ] = None,
    transformation_type: Annotated[
        Optional[str],
        typer.Option(
            "--transformation-type",
            help="Transformation type (e.g. 'rigid3D', 'affine3D', 'vectorfield3D').",
        ),
    ] = None,
    template: Annotated[
        Optional[Path],
        typer.Option("--template", help="Template image for vector field geometry."),
    ] = None,
    floating: Annotated[
        Optional[Path],
        typer.Option("--floating", "-f", help="Floating image for unit conversion."),
    ] = None,
    input_unit: Annotated[
        Optional[str],
        typer.Option("--input-unit", help="Input unit: 'voxel' or 'real'."),
    ] = None,
    output_unit: Annotated[
        Optional[str],
        typer.Option("--output-unit", help="Output unit: 'voxel' or 'real'."),
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
            help="Print the original copyTrsf help and exit.",
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
    """Copy and convert transformations."""
    setup_logger(log_level)
    tool_logger = logger.bind(executable="copyTrsf")

    args: list[str] = []
    if input_trsf is not None:
        args.append(str(input_trsf))
    if output_trsf is not None:
        args.append(str(output_trsf))
    if transformation_type is not None:
        args.extend(["-trsf-type", transformation_type])
    if template is not None:
        args.extend(["-t", str(template)])
    if floating is not None:
        args.extend(["-flo", str(floating)])
    if input_unit is not None:
        args.extend(["-iu", input_unit])
    if output_unit is not None:
        args.extend(["-ou", output_unit])
    if verbose:
        args.append("-v")
    if no_verbose:
        args.append("-nv")

    run("copyTrsf", *args, tool_logger=tool_logger)

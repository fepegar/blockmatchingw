"""CLI command for invTrsf."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from loguru import logger

from blockmatchingw.commands import make_help_callback, setup_logger
from blockmatchingw.enums import LogLevel
from blockmatchingw.wrapper import run

_help_callback = make_help_callback("invTrsf")


def inv_trsf(
    input_trsf: Annotated[
        Optional[Path],
        typer.Option("--input", "-i", help="Input transformation."),
    ] = None,
    output_trsf: Annotated[
        Optional[Path],
        typer.Option("--output", "-o", help="Output inverted transformation."),
    ] = None,
    template: Annotated[
        Optional[Path],
        typer.Option("--template", help="Template image for vector field geometry."),
    ] = None,
    input_unit: Annotated[
        Optional[str],
        typer.Option("--input-unit", help="Transformation unit: 'voxel' or 'real'."),
    ] = None,
    inversion_error: Annotated[
        Optional[float],
        typer.Option("--inversion-error", help="Absolute error for convergence."),
    ] = None,
    inversion_iteration: Annotated[
        Optional[int],
        typer.Option("--inversion-iteration", help="Max iterations for convergence."),
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
            help="Print the original invTrsf help and exit.",
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
    """Invert a transformation."""
    setup_logger(log_level)
    tool_logger = logger.bind(executable="invTrsf")

    args: list[str] = []
    if input_trsf is not None:
        args.append(str(input_trsf))
    if output_trsf is not None:
        args.append(str(output_trsf))
    if template is not None:
        args.extend(["-t", str(template)])
    if input_unit is not None:
        args.extend(["-iu", input_unit])
    if inversion_error is not None:
        args.extend(["-inversion-error", str(inversion_error)])
    if inversion_iteration is not None:
        args.extend(["-inversion-iteration", str(inversion_iteration)])
    if verbose:
        args.append("-v")
    if no_verbose:
        args.append("-nv")

    run("invTrsf", *args, tool_logger=tool_logger)

"""CLI command for createTrsf."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from loguru import logger

from blockmatchingw.commands import make_help_callback, setup_logger
from blockmatchingw.enums import LogLevel
from blockmatchingw.wrapper import run

_help_callback = make_help_callback("createTrsf")


def create_trsf(
    result: Annotated[
        Optional[Path],
        typer.Option("--result", help="Output transformation."),
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
    value: Annotated[
        Optional[str],
        typer.Option(
            "--value",
            help="Transformation value: 'identity', 'random', 'sinus2D', 'sinus3D'.",
        ),
    ] = None,
    identity: Annotated[
        bool,
        typer.Option("--identity", help="Create identity transformation."),
    ] = False,
    random: Annotated[
        bool,
        typer.Option("--random", help="Create random transformation."),
    ] = False,
    print_transformation: Annotated[
        bool,
        typer.Option(
            "--print-transformation", help="Print the created transformation."
        ),
    ] = False,
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
            help="Print the original createTrsf help and exit.",
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
    """Create a transformation from scratch."""
    setup_logger(log_level)
    tool_logger = logger.bind(executable="createTrsf")

    args: list[str] = []
    if result is not None:
        args.extend(["-res", str(result)])
    if transformation_type is not None:
        args.extend(["-trsf-type", transformation_type])
    if template is not None:
        args.extend(["-t", str(template)])
    if value is not None:
        args.extend(["-value", value])
    if identity:
        args.append("-id")
    if random:
        args.append("-rand")
    if print_transformation:
        args.append("-print")
    if verbose:
        args.append("-v")
    if no_verbose:
        args.append("-nv")

    run("createTrsf", *args, tool_logger=tool_logger)

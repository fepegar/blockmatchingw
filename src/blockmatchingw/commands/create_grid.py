"""CLI command for createGrid."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from loguru import logger

from blockmatchingw.commands import make_help_callback, setup_logger
from blockmatchingw.enums import LogLevel
from blockmatchingw.wrapper import run

_help_callback = make_help_callback("createGrid")


def create_grid(
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Output grid image."),
    ],
    input_image: Annotated[
        Optional[Path],
        typer.Option("--input", "-i", help="Input image."),
    ] = None,
    template: Annotated[
        Optional[Path],
        typer.Option("--template", help="Template image for dimensions."),
    ] = None,
    grid_type: Annotated[
        Optional[str],
        typer.Option("--grid-type", help="Output type: 'grid' or 'mosaic'."),
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
            help="Print the original createGrid help and exit.",
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
    """Create a deformation grid."""
    setup_logger(log_level)
    tool_logger = logger.bind(executable="createGrid")

    args: list[str] = []
    if input_image is not None:
        args.append(str(input_image))
    args.append(str(output))
    if template is not None:
        args.extend(["-t", str(template)])
    if grid_type is not None:
        args.extend(["-type", grid_type])
    if verbose:
        args.append("-v")
    if no_verbose:
        args.append("-nv")

    run("createGrid", *args, tool_logger=tool_logger)

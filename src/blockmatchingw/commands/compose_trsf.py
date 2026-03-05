"""CLI command for composeTrsf."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from loguru import logger

from blockmatchingw.commands import make_help_callback, setup_logger
from blockmatchingw.enums import LogLevel
from blockmatchingw.wrapper import run

_help_callback = make_help_callback("composeTrsf")


def compose_trsf(
    result: Annotated[
        Optional[Path],
        typer.Option("--result", help="Output transformation."),
    ] = None,
    transformations: Annotated[
        Optional[list[Path]],
        typer.Option(
            "--transformation",
            "-t",
            help="Input transformation files (repeat for multiple).",
        ),
    ] = None,
    transformation_list: Annotated[
        Optional[Path],
        typer.Option(
            "--transformation-list",
            help="Text file containing transformation file names.",
        ),
    ] = None,
    transformation_format: Annotated[
        Optional[str],
        typer.Option(
            "--transformation-format",
            help="Format 'a la printf' for transformation file names.",
        ),
    ] = None,
    first: Annotated[
        Optional[int],
        typer.Option("--first", help="First index for format."),
    ] = None,
    last: Annotated[
        Optional[int],
        typer.Option("--last", help="Last index for format."),
    ] = None,
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
            help="Print the original composeTrsf help and exit.",
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
    """Compose multiple transformations into one."""
    setup_logger(log_level)
    tool_logger = logger.bind(executable="composeTrsf")

    args: list[str] = []
    if result is not None:
        args.extend(["-res", str(result)])
    if transformations is not None:
        args.append("-trsfs")
        for t in transformations:
            args.append(str(t))
    if transformation_list is not None:
        args.extend(["-trsf-list", str(transformation_list)])
    if transformation_format is not None:
        args.extend(["-trsf-format", str(transformation_format)])
    if first is not None:
        args.extend(["-f", str(first)])
    if last is not None:
        args.extend(["-l", str(last)])
    if template is not None:
        args.extend(["-t", str(template)])
    if verbose:
        args.append("-v")
    if no_verbose:
        args.append("-nv")

    run("composeTrsf", *args, tool_logger=tool_logger)

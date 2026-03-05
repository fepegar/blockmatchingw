"""CLI command for cropImage."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from loguru import logger

from blockmatchingw.commands import make_help_callback, setup_logger
from blockmatchingw.enums import LogLevel
from blockmatchingw.wrapper import run

_help_callback = make_help_callback("cropImage")


def crop_image(
    input_image: Annotated[
        Path,
        typer.Option("--input", "-i", help="Input image."),
    ],
    output_image: Annotated[
        Optional[Path],
        typer.Option("--output", "-o", help="Output cropped image."),
    ] = None,
    template: Annotated[
        Optional[Path],
        typer.Option("--template", help="Template image for crop dimensions."),
    ] = None,
    origin_x: Annotated[
        Optional[int],
        typer.Option("--origin-x", help="Origin along X."),
    ] = None,
    origin_y: Annotated[
        Optional[int],
        typer.Option("--origin-y", help="Origin along Y."),
    ] = None,
    origin_z: Annotated[
        Optional[int],
        typer.Option("--origin-z", help="Origin along Z."),
    ] = None,
    dim_x: Annotated[
        Optional[int],
        typer.Option("--dim-x", help="Dimension along X."),
    ] = None,
    dim_y: Annotated[
        Optional[int],
        typer.Option("--dim-y", help="Dimension along Y."),
    ] = None,
    dim_z: Annotated[
        Optional[int],
        typer.Option("--dim-z", help="Dimension along Z."),
    ] = None,
    xy_slice: Annotated[
        Optional[int],
        typer.Option("--xy", help="Extract XY slice at this index."),
    ] = None,
    xz_slice: Annotated[
        Optional[int],
        typer.Option("--xz", help="Extract XZ slice at this index."),
    ] = None,
    yz_slice: Annotated[
        Optional[int],
        typer.Option("--yz", help="Extract YZ slice at this index."),
    ] = None,
    result_transformation: Annotated[
        Optional[Path],
        typer.Option(
            "--result-transformation",
            help="Resampling transformation output.",
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
            help="Print the original cropImage help and exit.",
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
    """Crop an image."""
    setup_logger(log_level)
    tool_logger = logger.bind(executable="cropImage")

    args: list[str] = [str(input_image)]
    if output_image is not None:
        args.append(str(output_image))
    if template is not None:
        args.extend(["-t", str(template)])
    if origin_x is not None:
        args.extend(["-ix", str(origin_x)])
    if origin_y is not None:
        args.extend(["-iy", str(origin_y)])
    if origin_z is not None:
        args.extend(["-iz", str(origin_z)])
    if dim_x is not None:
        args.extend(["-x", str(dim_x)])
    if dim_y is not None:
        args.extend(["-y", str(dim_y)])
    if dim_z is not None:
        args.extend(["-z", str(dim_z)])
    if xy_slice is not None:
        args.extend(["-xy", str(xy_slice)])
    if xz_slice is not None:
        args.extend(["-xz", str(xz_slice)])
    if yz_slice is not None:
        args.extend(["-yz", str(yz_slice)])
    if result_transformation is not None:
        args.extend(["-res-trsf", str(result_transformation)])
    if verbose:
        args.append("-v")
    if no_verbose:
        args.append("-nv")

    run("cropImage", *args, tool_logger=tool_logger)

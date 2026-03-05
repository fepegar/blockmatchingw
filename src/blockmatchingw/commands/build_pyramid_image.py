"""CLI command for buildPyramidImage."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from loguru import logger

from blockmatchingw.commands import make_help_callback, setup_logger
from blockmatchingw.enums import LogLevel
from blockmatchingw.wrapper import run

_help_callback = make_help_callback("buildPyramidImage")


def build_pyramid_image(
    input_image: Annotated[
        Path,
        typer.Option("--input", "-i", help="Input image."),
    ],
    result_image_format: Annotated[
        Optional[str],
        typer.Option(
            "--result-image-format",
            help="Format 'a la printf' for output images (must contain '%d').",
        ),
    ] = None,
    normalisation: Annotated[
        Optional[bool],
        typer.Option(
            "--normalisation/--no-normalisation",
            help="Normalize input image on one byte.",
        ),
    ] = None,
    pyramid_lowest_level: Annotated[
        Optional[int],
        typer.Option(
            "--pyramid-lowest-level",
            help="Pyramid lowest level (0 = original dimension).",
        ),
    ] = None,
    pyramid_highest_level: Annotated[
        Optional[int],
        typer.Option("--pyramid-highest-level", help="Pyramid highest level."),
    ] = None,
    pyramid_gaussian_filtering: Annotated[
        bool,
        typer.Option(
            "--pyramid-gaussian-filtering",
            help="Apply Gaussian filtering before subsampling.",
        ),
    ] = False,
    gaussian_filter_type: Annotated[
        Optional[str],
        typer.Option(
            "--gaussian-filter-type",
            help="Filter type for Gaussian filtering.",
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
            help="Print the original buildPyramidImage help and exit.",
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
    """Build multi-resolution image pyramids."""
    setup_logger(log_level)
    tool_logger = logger.bind(executable="buildPyramidImage")

    args: list[str] = [str(input_image)]
    if result_image_format is not None:
        args.extend(["-res-image", result_image_format])
    if normalisation is True:
        args.append("-normalisation")
    elif normalisation is False:
        args.append("-no-normalisation")
    if pyramid_lowest_level is not None:
        args.extend(["-py-ll", str(pyramid_lowest_level)])
    if pyramid_highest_level is not None:
        args.extend(["-py-hl", str(pyramid_highest_level)])
    if pyramid_gaussian_filtering:
        args.append("-py-gf")
    if gaussian_filter_type is not None:
        args.extend(["-filter-type", gaussian_filter_type])
    if verbose:
        args.append("-v")
    if no_verbose:
        args.append("-nv")

    run("buildPyramidImage", *args, tool_logger=tool_logger)

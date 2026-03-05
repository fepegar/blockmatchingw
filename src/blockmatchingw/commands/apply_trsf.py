"""CLI command for applyTrsf."""

from pathlib import Path
from typing import Annotated, Optional

import typer

from blockmatchingw.commands import make_help_callback, setup_logger
from blockmatchingw.enums import LogLevel
from blockmatchingw.wrapper import apply_trsf as _apply_trsf

_help_callback = make_help_callback("applyTrsf")


def apply_trsf(
    floating: Annotated[
        Path,
        typer.Option("--floating", "-f", help="Input image to be resampled."),
    ],
    result: Annotated[
        Optional[Path],
        typer.Option("--result", help="Result image path."),
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
    result_transformation: Annotated[
        Optional[Path],
        typer.Option(
            "--result-transformation",
            help="Applied transformation output in real coordinates.",
        ),
    ] = None,
    result_voxel_transformation: Annotated[
        Optional[Path],
        typer.Option(
            "--result-voxel-transformation",
            help="Applied transformation output in voxel coordinates.",
        ),
    ] = None,
    default_transformation: Annotated[
        Optional[str],
        typer.Option(
            "--default-transformation",
            help="Default transformation: 'identity' or 'fovcenter'.",
        ),
    ] = None,
    reference: Annotated[
        Optional[Path],
        typer.Option(
            "--reference",
            "-r",
            help="Template/reference image for output geometry.",
        ),
    ] = None,
    interpolation: Annotated[
        Optional[str],
        typer.Option(
            "--interpolation",
            help="Interpolation mode: 'nearest', 'linear', or 'cspline'.",
        ),
    ] = None,
    resize: Annotated[
        bool,
        typer.Option("--resize", help="Resize output to match input field of view."),
    ] = False,
    isotropic_voxel: Annotated[
        Optional[float],
        typer.Option("--isotropic-voxel", help="Isotropic voxel size."),
    ] = None,
    output_type: Annotated[
        Optional[str],
        typer.Option("--output-type", help="Output image type."),
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
            help="Print the original applyTrsf help and exit.",
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
    """Apply a transformation to an image."""
    setup_logger(log_level)
    _apply_trsf(
        floating,
        result=result,
        transformation=transformation,
        voxel_transformation=voxel_transformation,
        result_transformation=result_transformation,
        result_voxel_transformation=result_voxel_transformation,
        default_transformation=default_transformation,
        reference=reference,
        interpolation=interpolation,
        resize=resize,
        isotropic_voxel=isotropic_voxel,
        output_type=output_type,
        verbose=verbose,
        no_verbose=no_verbose,
    )

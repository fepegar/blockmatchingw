"""CLI command for blockmatching."""

from pathlib import Path
from typing import Annotated, Optional

import typer

from blockmatchingw.commands import make_help_callback, setup_logger
from blockmatchingw.enums import LogLevel
from blockmatchingw.wrapper import blockmatching as _blockmatching

_help_callback = make_help_callback("blockmatching")


def blockmatching(
    reference: Annotated[
        Path,
        typer.Option("--reference", "-r", help="Reference (still) image."),
    ],
    floating: Annotated[
        Path,
        typer.Option("--floating", "-f", help="Floating image to be registered."),
    ],
    result: Annotated[
        Optional[Path],
        typer.Option("--result", help="Result image path."),
    ] = None,
    result_transformation: Annotated[
        Optional[Path],
        typer.Option(
            "--result-transformation",
            help="Output transformation in real coordinates.",
        ),
    ] = None,
    result_voxel_transformation: Annotated[
        Optional[Path],
        typer.Option(
            "--result-voxel-transformation",
            help="Output transformation in voxel coordinates.",
        ),
    ] = None,
    initial_transformation: Annotated[
        Optional[Path],
        typer.Option(
            "--initial-transformation",
            help="Initial/left transformation in real coordinates.",
        ),
    ] = None,
    initial_voxel_transformation: Annotated[
        Optional[Path],
        typer.Option(
            "--initial-voxel-transformation",
            help="Initial/left transformation in voxel coordinates.",
        ),
    ] = None,
    initial_result_transformation: Annotated[
        Optional[Path],
        typer.Option(
            "--initial-result-transformation",
            help="Initialization of result transformation in real coordinates.",
        ),
    ] = None,
    initial_result_voxel_transformation: Annotated[
        Optional[Path],
        typer.Option(
            "--initial-result-voxel-transformation",
            help="Initialization of result transformation in voxel coordinates.",
        ),
    ] = None,
    default_transformation: Annotated[
        Optional[str],
        typer.Option(
            "--default-transformation",
            help="Default transformation: 'identity' or 'fovcenter'.",
        ),
    ] = None,
    normalisation: Annotated[
        Optional[bool],
        typer.Option(
            "--normalisation/--no-normalisation",
            help="Normalize images before registration.",
        ),
    ] = None,
    composition_with_initial: Annotated[
        Optional[bool],
        typer.Option(
            "--composition-with-initial/--no-composition-with-initial",
            help="Compose result with initial transformation.",
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
    similarity_measure: Annotated[
        Optional[str],
        typer.Option("--similarity-measure", help="Similarity measure (e.g. 'cc')."),
    ] = None,
    similarity_measure_threshold: Annotated[
        Optional[float],
        typer.Option(
            "--similarity-measure-threshold", help="Similarity measure threshold."
        ),
    ] = None,
    transformation_type: Annotated[
        Optional[str],
        typer.Option(
            "--transformation-type",
            help="Transformation type (e.g. 'rigid3D', 'affine3D').",
        ),
    ] = None,
    estimator_type: Annotated[
        Optional[str],
        typer.Option(
            "--estimator-type",
            help="Estimator type: 'wlts', 'lts', 'wls', or 'ls'.",
        ),
    ] = None,
    lts_cut: Annotated[
        Optional[float],
        typer.Option("--lts-cut", help="LTS cut/fraction."),
    ] = None,
    max_iterations: Annotated[
        Optional[int],
        typer.Option("--max-iterations", help="Maximum iterations."),
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
            help="Print the original blockmatching help and exit.",
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
    """Block matching-based image registration."""
    setup_logger(log_level)
    _blockmatching(
        reference,
        floating,
        result=result,
        result_transformation=result_transformation,
        result_voxel_transformation=result_voxel_transformation,
        initial_transformation=initial_transformation,
        initial_voxel_transformation=initial_voxel_transformation,
        initial_result_transformation=initial_result_transformation,
        initial_result_voxel_transformation=initial_result_voxel_transformation,
        default_transformation=default_transformation,
        normalisation=normalisation,
        composition_with_initial=composition_with_initial,
        pyramid_lowest_level=pyramid_lowest_level,
        pyramid_highest_level=pyramid_highest_level,
        pyramid_gaussian_filtering=pyramid_gaussian_filtering,
        similarity_measure=similarity_measure,
        similarity_measure_threshold=similarity_measure_threshold,
        transformation_type=transformation_type,
        estimator_type=estimator_type,
        lts_cut=lts_cut,
        max_iterations=max_iterations,
        verbose=verbose,
        no_verbose=no_verbose,
    )

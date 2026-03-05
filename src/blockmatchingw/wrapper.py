"""Python wrapper for Klab-BlockMatching binaries."""

from __future__ import annotations

from pathlib import Path
from subprocess import PIPE, Popen
from threading import Thread
from typing import TextIO

import loguru
from loguru import logger

from .install import find as _find


def _get_path(tool: str) -> Path:
    path = _find(tool)
    if path is None:
        msg = (
            f"{tool} not found. Please install BlockMatching first"
            " by running: blockmatchingw install"
        )
        raise FileNotFoundError(msg)
    return path


def _read_stream(
    stream: TextIO,
    is_stderr: bool,
    tool_logger: loguru.Logger | None,
) -> None:
    for line in stream:
        line = line.rstrip("\n")
        if tool_logger is None:
            logger.info(line)
        elif is_stderr:
            tool_logger.warning(line)
        else:
            tool_logger.info(line)


def run(tool: str, *args: str, tool_logger: loguru.Logger | None = None) -> None:
    """Run any Klab-BlockMatching binary with raw CLI arguments.

    Args:
        tool: Binary name (e.g. ``"blockmatching"``).
        *args: Raw CLI arguments.
        tool_logger: Optional loguru logger for structured output.
    """
    tool_path = _get_path(tool)
    args_list = [arg.strip("\\\n") for arg in args]
    args_list = [arg for arg in args_list if arg]

    cmd = [str(tool_path), *args_list]
    with Popen(cmd, stdout=PIPE, stderr=PIPE, text=True, bufsize=1) as p:
        assert p.stdout is not None
        assert p.stderr is not None

        stderr_thread = Thread(
            target=_read_stream,
            args=(p.stderr, True, tool_logger),
            name="stderr-reader",
        )
        stdout_thread = Thread(
            target=_read_stream,
            args=(p.stdout, False, tool_logger),
            name="stdout-reader",
        )

        stderr_thread.start()
        stdout_thread.start()

        stderr_thread.join()
        stdout_thread.join()

        p.wait()


def _run_with_logging(tool: str, *lines: str) -> None:
    tool_path = _get_path(tool)
    loggerw = logger.bind(executable="blockmatchingw")
    loggerx = logger.bind(executable=tool)

    loggerw.debug("The following command will be run:")
    lines_str = "\n".join(lines).strip(" \\")
    loggerw.debug(f"{tool_path} \\\n  {lines_str}")
    args = []
    for line in lines:
        args.extend(line.strip(" \\").split())

    run(tool, *args, tool_logger=loggerx)


def blockmatching(
    reference: Path,
    floating: Path,
    *,
    result: Path | None = None,
    result_transformation: Path | None = None,
    result_voxel_transformation: Path | None = None,
    initial_transformation: Path | None = None,
    initial_voxel_transformation: Path | None = None,
    initial_result_transformation: Path | None = None,
    initial_result_voxel_transformation: Path | None = None,
    default_transformation: str | None = None,
    normalisation: bool | None = None,
    composition_with_initial: bool | None = None,
    pyramid_lowest_level: int | None = None,
    pyramid_highest_level: int | None = None,
    pyramid_gaussian_filtering: bool = False,
    block_size: tuple[int, int, int] | None = None,
    block_spacing: tuple[int, int, int] | None = None,
    block_border: tuple[int, int, int] | None = None,
    floating_low_threshold: int | None = None,
    floating_high_threshold: int | None = None,
    floating_removed_fraction: float | None = None,
    reference_low_threshold: int | None = None,
    reference_high_threshold: int | None = None,
    reference_removed_fraction: float | None = None,
    floating_selection_fraction: float | None = None,
    search_neighborhood_half_size: tuple[int, int, int] | None = None,
    search_neighborhood_step: tuple[int, int, int] | None = None,
    similarity_measure: str | None = None,
    similarity_measure_threshold: float | None = None,
    transformation_type: str | None = None,
    elastic_regularization_sigma: tuple[float, float, float] | None = None,
    estimator_type: str | None = None,
    lts_cut: float | None = None,
    lts_deviation: float | None = None,
    lts_iterations: int | None = None,
    fluid_sigma: tuple[float, float, float] | None = None,
    vector_propagation_distance: float | None = None,
    vector_fading_distance: float | None = None,
    max_iterations: int | None = None,
    corner_ending_condition: bool = False,
    gaussian_filter_type: str | None = None,
    command_line: Path | None = None,
    logfile: Path | None = None,
    verbose: bool = False,
    no_verbose: bool = False,
    parallel: bool | None = None,
    max_chunks: int | None = None,
    parallelism_type: str | None = None,
) -> None:
    """Run block matching-based image registration.

    Args:
        reference: Reference (still) image path.
        floating: Floating image path to be registered.
        result: Output result image path.
        result_transformation: Output transformation in real coordinates.
        result_voxel_transformation: Output transformation in voxel coordinates.
        initial_transformation: Initial/left transformation in real coordinates.
        initial_voxel_transformation: Initial/left transformation in voxel
            coordinates.
        initial_result_transformation: Initialization of result transformation
            in real coordinates.
        initial_result_voxel_transformation: Initialization of result
            transformation in voxel coordinates.
        default_transformation: Default transformation (``"identity"`` or
            ``"fovcenter"``).
        normalisation: If ``True``, normalize images; if ``False``, do not.
        composition_with_initial: If ``True``, compose with initial; if
            ``False``, do not.
        pyramid_lowest_level: Pyramid lowest level (0 = original).
        pyramid_highest_level: Pyramid highest level.
        pyramid_gaussian_filtering: Apply Gaussian filtering before
            subsampling.
        block_size: Block size ``(x, y, z)``.
        block_spacing: Block spacing ``(x, y, z)``.
        block_border: Block border ``(x, y, z)``.
        floating_low_threshold: Low threshold for floating image.
        floating_high_threshold: High threshold for floating image.
        floating_removed_fraction: Removed fraction for floating image.
        reference_low_threshold: Low threshold for reference image.
        reference_high_threshold: High threshold for reference image.
        reference_removed_fraction: Removed fraction for reference image.
        floating_selection_fraction: Selection fraction for floating image.
        search_neighborhood_half_size: Search neighborhood half size
            ``(x, y, z)``.
        search_neighborhood_step: Search neighborhood step ``(x, y, z)``.
        similarity_measure: Similarity measure (e.g. ``"cc"``).
        similarity_measure_threshold: Similarity measure threshold.
        transformation_type: Transformation type (e.g. ``"rigid3D"``,
            ``"affine3D"``).
        elastic_regularization_sigma: Elastic regularization sigma
            ``(x, y, z)``.
        estimator_type: Estimator type (``"wlts"``, ``"lts"``, ``"wls"``,
            ``"ls"``).
        lts_cut: LTS cut/fraction.
        lts_deviation: LTS deviation.
        lts_iterations: LTS iterations.
        fluid_sigma: Fluid sigma ``(x, y, z)``.
        vector_propagation_distance: Vector propagation distance.
        vector_fading_distance: Vector fading distance.
        max_iterations: Maximum iterations.
        corner_ending_condition: Use corner ending condition (RMS).
        gaussian_filter_type: Filter type for Gaussian filtering.
        command_line: File to write command line to.
        logfile: Log file path.
        verbose: Enable verbose output.
        no_verbose: Disable verbose output.
        parallel: Enable or disable parallelism.
        max_chunks: Maximum number of chunks for parallel processing.
        parallelism_type: Parallelism type.
    """
    lines: list[str] = [
        f"-ref {reference} \\",
        f"-flo {floating} \\",
    ]
    if result is not None:
        lines.append(f"-res {result} \\")
    if result_transformation is not None:
        lines.append(f"-res-trsf {result_transformation} \\")
    if result_voxel_transformation is not None:
        lines.append(f"-res-voxel-trsf {result_voxel_transformation} \\")
    if initial_transformation is not None:
        lines.append(f"-init-trsf {initial_transformation} \\")
    if initial_voxel_transformation is not None:
        lines.append(f"-init-voxel-trsf {initial_voxel_transformation} \\")
    if initial_result_transformation is not None:
        lines.append(f"-init-res-trsf {initial_result_transformation} \\")
    if initial_result_voxel_transformation is not None:
        lines.append(f"-init-res-voxel-trsf {initial_result_voxel_transformation} \\")
    if default_transformation is not None:
        lines.append(f"-default-trsf {default_transformation} \\")
    if normalisation is True:
        lines.append("-normalisation \\")
    elif normalisation is False:
        lines.append("-no-normalisation \\")
    if composition_with_initial is True:
        lines.append("-composition-with-initial \\")
    elif composition_with_initial is False:
        lines.append("-no-composition-with-initial \\")
    if pyramid_lowest_level is not None:
        lines.append(f"-py-ll {pyramid_lowest_level} \\")
    if pyramid_highest_level is not None:
        lines.append(f"-py-hl {pyramid_highest_level} \\")
    if pyramid_gaussian_filtering:
        lines.append("-py-gf \\")
    if block_size is not None:
        lines.append(f"-bl-size {block_size[0]} {block_size[1]} {block_size[2]} \\")
    if block_spacing is not None:
        lines.append(
            f"-bl-space {block_spacing[0]} {block_spacing[1]} {block_spacing[2]} \\"
        )
    if block_border is not None:
        lines.append(
            f"-bl-border {block_border[0]} {block_border[1]} {block_border[2]} \\"
        )
    if floating_low_threshold is not None:
        lines.append(f"-flo-lt {floating_low_threshold} \\")
    if floating_high_threshold is not None:
        lines.append(f"-flo-ht {floating_high_threshold} \\")
    if floating_removed_fraction is not None:
        lines.append(f"-flo-rf {floating_removed_fraction} \\")
    if reference_low_threshold is not None:
        lines.append(f"-ref-lt {reference_low_threshold} \\")
    if reference_high_threshold is not None:
        lines.append(f"-ref-ht {reference_high_threshold} \\")
    if reference_removed_fraction is not None:
        lines.append(f"-ref-rf {reference_removed_fraction} \\")
    if floating_selection_fraction is not None:
        lines.append(f"-flo-frac {floating_selection_fraction} \\")
    if search_neighborhood_half_size is not None:
        s = search_neighborhood_half_size
        lines.append(f"-se-hsize {s[0]} {s[1]} {s[2]} \\")
    if search_neighborhood_step is not None:
        s = search_neighborhood_step
        lines.append(f"-se-step {s[0]} {s[1]} {s[2]} \\")
    if similarity_measure is not None:
        lines.append(f"-si {similarity_measure} \\")
    if similarity_measure_threshold is not None:
        lines.append(f"-si-th {similarity_measure_threshold} \\")
    if transformation_type is not None:
        lines.append(f"-trsf-type {transformation_type} \\")
    if elastic_regularization_sigma is not None:
        e = elastic_regularization_sigma
        lines.append(f"-elastic-sigma {e[0]} {e[1]} {e[2]} \\")
    if estimator_type is not None:
        lines.append(f"-es-type {estimator_type} \\")
    if lts_cut is not None:
        lines.append(f"-lts-cut {lts_cut} \\")
    if lts_deviation is not None:
        lines.append(f"-lts-deviation {lts_deviation} \\")
    if lts_iterations is not None:
        lines.append(f"-lts-iterations {lts_iterations} \\")
    if fluid_sigma is not None:
        lines.append(
            f"-lts-sigma {fluid_sigma[0]} {fluid_sigma[1]} {fluid_sigma[2]} \\"
        )
    if vector_propagation_distance is not None:
        lines.append(f"-pdistance {vector_propagation_distance} \\")
    if vector_fading_distance is not None:
        lines.append(f"-fdistance {vector_fading_distance} \\")
    if max_iterations is not None:
        lines.append(f"-max-iterations {max_iterations} \\")
    if corner_ending_condition:
        lines.append("-rms \\")
    if gaussian_filter_type is not None:
        lines.append(f"-filter-type {gaussian_filter_type} \\")
    if command_line is not None:
        lines.append(f"-command-line {command_line} \\")
    if logfile is not None:
        lines.append(f"-logfile {logfile} \\")
    if verbose:
        lines.append("-v \\")
    if no_verbose:
        lines.append("-nv \\")
    if parallel is True:
        lines.append("-parallel \\")
    elif parallel is False:
        lines.append("-no-parallel \\")
    if max_chunks is not None:
        lines.append(f"-max-chunks {max_chunks} \\")
    if parallelism_type is not None:
        lines.append(f"-parallel-type {parallelism_type} \\")

    _run_with_logging("blockmatching", *lines)


def apply_trsf(
    floating: Path,
    *,
    result: Path | None = None,
    transformation: Path | None = None,
    voxel_transformation: Path | None = None,
    result_transformation: Path | None = None,
    result_voxel_transformation: Path | None = None,
    default_transformation: str | None = None,
    reference: Path | None = None,
    template_dimensions: tuple[int, ...] | None = None,
    voxel_size: tuple[float, ...] | None = None,
    floating_voxel: tuple[float, ...] | None = None,
    resize: bool = False,
    isotropic_voxel: float | None = None,
    interpolation: str | None = None,
    nearest: bool = False,
    linear: bool = False,
    cspline: bool = False,
    output_type: str | None = None,
    verbose: bool = False,
    no_verbose: bool = False,
    parallel: bool | None = None,
    max_chunks: int | None = None,
    parallelism_type: str | None = None,
) -> None:
    """Apply a transformation to an image.

    Args:
        floating: Input image to be resampled.
        result: Result image path.
        transformation: Transformation file in real coordinates.
        voxel_transformation: Transformation file in voxel coordinates.
        result_transformation: Applied transformation output in real
            coordinates.
        result_voxel_transformation: Applied transformation output in voxel
            coordinates.
        default_transformation: Default transformation (``"identity"`` or
            ``"fovcenter"``).
        reference: Template/reference image for output geometry.
        template_dimensions: Dimensions of the result image.
        voxel_size: Voxel sizes of the result image.
        floating_voxel: Voxel sizes of the input image.
        resize: Resize the output to match input field of view.
        isotropic_voxel: Isotropic voxel size (shortcut for resize + voxel).
        interpolation: Interpolation mode (``"nearest"``, ``"linear"``,
            ``"cspline"``).
        nearest: Use nearest neighbor interpolation.
        linear: Use bilinear/trilinear interpolation.
        cspline: Use cubic spline interpolation.
        output_type: Output image type.
        verbose: Enable verbose output.
        no_verbose: Disable verbose output.
        parallel: Enable or disable parallelism.
        max_chunks: Maximum chunks for parallel processing.
        parallelism_type: Parallelism type.
    """
    lines: list[str] = [
        f"-flo {floating} \\",
    ]
    if result is not None:
        lines.append(f"-res {result} \\")
    if transformation is not None:
        lines.append(f"-trsf {transformation} \\")
    if voxel_transformation is not None:
        lines.append(f"-voxel-trsf {voxel_transformation} \\")
    if result_transformation is not None:
        lines.append(f"-res-trsf {result_transformation} \\")
    if result_voxel_transformation is not None:
        lines.append(f"-res-voxel-trsf {result_voxel_transformation} \\")
    if default_transformation is not None:
        lines.append(f"-default-trsf {default_transformation} \\")
    if reference is not None:
        lines.append(f"-ref {reference} \\")
    if template_dimensions is not None:
        dims = " ".join(str(d) for d in template_dimensions)
        lines.append(f"-dim {dims} \\")
    if voxel_size is not None:
        vs = " ".join(str(v) for v in voxel_size)
        lines.append(f"-vs {vs} \\")
    if floating_voxel is not None:
        fv = " ".join(str(v) for v in floating_voxel)
        lines.append(f"-floating-voxel {fv} \\")
    if resize:
        lines.append("-resize \\")
    if isotropic_voxel is not None:
        lines.append(f"-iso {isotropic_voxel} \\")
    if interpolation is not None:
        lines.append(f"-interpolation {interpolation} \\")
    if nearest:
        lines.append("-nearest \\")
    if linear:
        lines.append("-linear \\")
    if cspline:
        lines.append("-cspline \\")
    if output_type is not None:
        lines.append(f"-type {output_type} \\")
    if verbose:
        lines.append("-v \\")
    if no_verbose:
        lines.append("-nv \\")
    if parallel is True:
        lines.append("-parallel \\")
    elif parallel is False:
        lines.append("-no-parallel \\")
    if max_chunks is not None:
        lines.append(f"-max-chunks {max_chunks} \\")
    if parallelism_type is not None:
        lines.append(f"-parallel-type {parallelism_type} \\")

    _run_with_logging("applyTrsf", *lines)

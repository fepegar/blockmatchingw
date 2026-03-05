"""Typer CLI for all Klab-BlockMatching binaries."""

import typer

from blockmatchingw.commands.apply_trsf import apply_trsf
from blockmatchingw.commands.apply_trsf_to_points import apply_trsf_to_points
from blockmatchingw.commands.blockmatching import blockmatching
from blockmatchingw.commands.build_pyramid_image import build_pyramid_image
from blockmatchingw.commands.compose_trsf import compose_trsf
from blockmatchingw.commands.copy_trsf import copy_trsf
from blockmatchingw.commands.create_grid import create_grid
from blockmatchingw.commands.create_trsf import create_trsf
from blockmatchingw.commands.crop_image import crop_image
from blockmatchingw.commands.install import install
from blockmatchingw.commands.intermediary_trsf import intermediary_trsf
from blockmatchingw.commands.interpolate_images import interpolate_images
from blockmatchingw.commands.inv_trsf import inv_trsf
from blockmatchingw.commands.pointmatching import pointmatching
from blockmatchingw.commands.print_image import print_image
from blockmatchingw.commands.print_trsf import print_trsf
from blockmatchingw.commands.test_libio_cmd import test_libio

app = typer.Typer(add_completion=False, no_args_is_help=True)

app.command(
    "install",
    help="Download and install BlockMatching binaries.",
)(install)

app.command(
    "blockmatching",
    help="Block matching-based image registration.",
    no_args_is_help=True,
)(blockmatching)
app.command(
    "apply-trsf",
    help="Apply a transformation to an image.",
    no_args_is_help=True,
)(apply_trsf)
app.command(
    "apply-trsf-to-points",
    help="Apply a transformation to point sets.",
    no_args_is_help=True,
)(apply_trsf_to_points)
app.command(
    "compose-trsf",
    help="Compose multiple transformations.",
    no_args_is_help=True,
)(compose_trsf)
app.command(
    "copy-trsf",
    help="Copy and convert transformations.",
    no_args_is_help=True,
)(copy_trsf)
app.command(
    "create-grid",
    help="Create a deformation grid.",
    no_args_is_help=True,
)(create_grid)
app.command(
    "create-trsf",
    help="Create a transformation.",
    no_args_is_help=True,
)(create_trsf)
app.command(
    "crop-image",
    help="Crop an image.",
    no_args_is_help=True,
)(crop_image)
app.command(
    "intermediary-trsf",
    help="Compute intermediary transformations.",
    no_args_is_help=True,
)(intermediary_trsf)
app.command(
    "interpolate-images",
    help="Interpolate between images.",
    no_args_is_help=True,
)(interpolate_images)
app.command(
    "inv-trsf",
    help="Invert a transformation.",
    no_args_is_help=True,
)(inv_trsf)
app.command(
    "pointmatching",
    help="Point matching-based registration.",
    no_args_is_help=True,
)(pointmatching)
app.command(
    "build-pyramid-image",
    help="Build multi-resolution image pyramids.",
    no_args_is_help=True,
)(build_pyramid_image)
app.command(
    "print-image",
    help="Print image information.",
)(print_image)
app.command(
    "print-trsf",
    help="Print transformation information.",
)(print_trsf)
app.command(
    "test-libio",
    help="Test I/O library.",
)(test_libio)


if __name__ == "__main__":
    app()

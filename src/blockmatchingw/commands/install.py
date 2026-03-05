"""CLI command for installing BlockMatching binaries."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from loguru import logger

from blockmatchingw.commands import setup_logger
from blockmatchingw.enums import LogLevel
from blockmatchingw.install import _DEFAULT_OUTPUT_DIR, download_blockmatching, get_platform


def install(
    output_dir: Annotated[
        Optional[Path],
        typer.Option(
            "--output-dir",
            "-o",
            help="Directory to install binaries into. Default: ~/.local/bin.",
        ),
    ] = None,
    show_platform: Annotated[
        bool,
        typer.Option(
            "--platform",
            help="Show the detected platform and exit without installing.",
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
    """Download and install BlockMatching binaries."""
    setup_logger(log_level)
    install_logger = logger.bind(executable="blockmatchingw")

    if show_platform:
        platform_name = get_platform()
        install_logger.info(f"Platform: {platform_name}")
        return

    out_dir = output_dir if output_dir is not None else _DEFAULT_OUTPUT_DIR
    installed = download_blockmatching(out_dir)
    for path in installed:
        install_logger.info(f"  Installed {path.name} → {path}")
    install_logger.info(f"Done! {len(installed)} binaries installed.")

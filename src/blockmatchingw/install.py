"""Download and install Klab-BlockMatching binaries."""

import platform
import shutil
import tarfile
import tempfile
from pathlib import Path

import requests
from loguru import logger

_GITHUB_URL = "https://github.com/fepegar/Klab-BlockMatching/releases/latest/download/klab-blockmatching-{platform}.tar.gz"

BINARIES = (
    "applyTrsf",
    "applyTrsfToPoints",
    "blockmatching",
    "buildPyramidImage",
    "composeTrsf",
    "copyTrsf",
    "createGrid",
    "createTrsf",
    "cropImage",
    "intermediaryTrsf",
    "interpolateImages",
    "invTrsf",
    "pointmatching",
    "printImage",
    "printTrsf",
    "test-libio",
)

_DEFAULT_OUTPUT_DIR = Path.home() / ".local" / "bin"


def get_platform() -> str:
    """Get the detected platform name for BlockMatching binary selection.

    Returns:
        Platform name string, one of: ``"linux-x86_64"``, ``"macos-arm64"``,
        or ``"macos-x86_64"``.
    """
    system = platform.system()
    match system:
        case "Linux":
            platform_name = "linux-x86_64"
        case "Darwin":
            if platform.processor() == "arm":
                platform_name = "macos-arm64"
            else:
                platform_name = "macos-x86_64"
        case _:
            raise Exception(f"Unsupported platform: {system}")
    return platform_name


def _get_download_url() -> str:
    platform_name = get_platform()
    return _GITHUB_URL.format(platform=platform_name)


def download_blockmatching(out_dir: Path = _DEFAULT_OUTPUT_DIR) -> list[Path]:
    """Download BlockMatching binaries and install them to *out_dir*.

    Args:
        out_dir: Directory where the binaries will be placed.
            Defaults to ``~/.local/bin``.

    Returns:
        List of paths to the installed binaries.
    """
    url = _get_download_url()
    download_logger = logger.bind(executable="blockmatchingw")
    download_logger.info(f"Downloading from {url}")
    response = requests.get(url)
    if response.status_code != 200:
        msg = f"Failed to download BlockMatching. Status code: {response.status_code}"
        raise RuntimeError(msg)

    tar_path = Path(tempfile.gettempdir(), "klab-blockmatching.tar.gz")
    with open(tar_path, "wb") as f:
        f.write(response.content)
    out_tmp_dir = Path(tempfile.gettempdir(), "klab-blockmatching")
    with tarfile.open(tar_path, "r:gz") as tar_ref:
        tar_ref.extractall(out_tmp_dir)

    out_dir.mkdir(parents=True, exist_ok=True)
    installed = []
    for path in out_tmp_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.name not in BINARIES:
            continue
        path.chmod(path.stat().st_mode | 0o111)
        dest = out_dir / path.name
        shutil.move(path, dest)
        installed.append(dest)

    # Clean up
    shutil.rmtree(out_tmp_dir, ignore_errors=True)
    tar_path.unlink(missing_ok=True)

    return sorted(installed)


def find(tool: str) -> Path | None:
    """Find a BlockMatching binary by name (e.g. ``"blockmatching"``)."""
    path = shutil.which(tool)
    return Path(path) if path else None

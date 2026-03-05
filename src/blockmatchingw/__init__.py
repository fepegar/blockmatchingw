from importlib.metadata import version

from .install import download_blockmatching, get_platform
from .wrapper import apply_trsf, blockmatching, run

__all__ = [
    "apply_trsf",
    "blockmatching",
    "download_blockmatching",
    "get_platform",
    "run",
]

assert __package__ is not None
__version__ = version(__package__)

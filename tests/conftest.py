"""Shared test fixtures."""

from pathlib import Path

import pytest


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture
def mock_image(tmp_path: Path) -> Path:
    """Create a minimal mock image file."""
    image_path = tmp_path / "test_image.nii.gz"
    image_path.write_bytes(b"\x00" * 64)
    return image_path


@pytest.fixture
def mock_trsf_file(tmp_path: Path) -> Path:
    """Create a mock transformation file."""
    trsf_path = tmp_path / "test_trsf.txt"
    trsf_path.write_text(
        "1.0 0.0 0.0 0.0\n0.0 1.0 0.0 0.0\n0.0 0.0 1.0 0.0\n0.0 0.0 0.0 1.0\n"
    )
    return trsf_path

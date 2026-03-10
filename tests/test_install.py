"""Tests for the install module."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from blockmatchingw.install import (
    BINARIES,
    _get_download_url,
    find,
    get_platform,
)


class TestGetPlatform:
    def test_linux(self) -> None:
        with patch("blockmatchingw.install.platform") as mock_platform:
            mock_platform.system.return_value = "Linux"
            assert get_platform() == "linux-x86_64"

    def test_macos_arm(self) -> None:
        with patch("blockmatchingw.install.platform") as mock_platform:
            mock_platform.system.return_value = "Darwin"
            mock_platform.processor.return_value = "arm"
            assert get_platform() == "macos-arm64"

    def test_macos_x86(self) -> None:
        with patch("blockmatchingw.install.platform") as mock_platform:
            mock_platform.system.return_value = "Darwin"
            mock_platform.processor.return_value = "i386"
            assert get_platform() == "macos-x86_64"

    def test_unsupported_platform(self) -> None:
        with patch("blockmatchingw.install.platform") as mock_platform:
            mock_platform.system.return_value = "Windows"
            with pytest.raises(Exception, match="Unsupported platform"):
                get_platform()


class TestGetDownloadUrl:
    def test_url_contains_platform(self) -> None:
        with patch("blockmatchingw.install.get_platform", return_value="linux-x86_64"):
            url = _get_download_url()
            assert "linux-x86_64" in url
            assert "github.com" in url
            assert "/releases/latest/download/" in url
            assert ".tar.gz" in url
            assert "v0.1.0" not in url


class TestFind:
    def test_returns_path_when_found(self) -> None:
        with patch("shutil.which", return_value="/usr/local/bin/blockmatching"):
            result = find("blockmatching")
            assert result == Path("/usr/local/bin/blockmatching")

    def test_returns_none_when_not_found(self) -> None:
        with patch("shutil.which", return_value=None):
            result = find("nonexistent")
            assert result is None


class TestBinaries:
    def test_contains_expected_tools(self) -> None:
        expected = [
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
        ]
        for tool in expected:
            assert tool in BINARIES, f"{tool} not in BINARIES"

    def test_binaries_is_tuple(self) -> None:
        assert isinstance(BINARIES, tuple)

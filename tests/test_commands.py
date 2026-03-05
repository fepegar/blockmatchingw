"""Tests for CLI commands."""

from __future__ import annotations

import re
from unittest.mock import patch

from typer.testing import CliRunner

from blockmatchingw.__main__ import app

runner = CliRunner()


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


class TestCLIHelp:
    def test_main_help(self) -> None:
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        output = _strip_ansi(result.output)
        assert "blockmatching" in output
        assert "apply-trsf" in output
        assert "install" in output

    def test_blockmatching_help(self) -> None:
        result = runner.invoke(app, ["blockmatching", "--help"])
        assert result.exit_code == 0
        output = _strip_ansi(result.output)
        assert "--reference" in output
        assert "--floating" in output

    def test_apply_trsf_help(self) -> None:
        result = runner.invoke(app, ["apply-trsf", "--help"])
        assert result.exit_code == 0
        output = _strip_ansi(result.output)
        assert "--floating" in output
        assert "--transformation" in output

    def test_compose_trsf_help(self) -> None:
        result = runner.invoke(app, ["compose-trsf", "--help"])
        assert result.exit_code == 0
        output = _strip_ansi(result.output)
        assert "--transformation" in output

    def test_inv_trsf_help(self) -> None:
        result = runner.invoke(app, ["inv-trsf", "--help"])
        assert result.exit_code == 0
        output = _strip_ansi(result.output)
        assert "--input" in output

    def test_create_trsf_help(self) -> None:
        result = runner.invoke(app, ["create-trsf", "--help"])
        assert result.exit_code == 0
        output = _strip_ansi(result.output)
        assert "--transformation-type" in output

    def test_crop_image_help(self) -> None:
        result = runner.invoke(app, ["crop-image", "--help"])
        assert result.exit_code == 0
        output = _strip_ansi(result.output)
        assert "--input" in output

    def test_print_image_help(self) -> None:
        result = runner.invoke(app, ["print-image", "--help"])
        assert result.exit_code == 0

    def test_print_trsf_help(self) -> None:
        result = runner.invoke(app, ["print-trsf", "--help"])
        assert result.exit_code == 0

    def test_all_commands_listed(self) -> None:
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        output = _strip_ansi(result.output)
        commands = [
            "blockmatching",
            "apply-trsf",
            "apply-trsf-to-points",
            "compose-trsf",
            "copy-trsf",
            "create-grid",
            "create-trsf",
            "crop-image",
            "intermediary-trsf",
            "interpolate-images",
            "inv-trsf",
            "pointmatching",
            "build-pyramid-image",
            "print-image",
            "print-trsf",
            "test-libio",
            "install",
        ]
        for cmd in commands:
            assert cmd in output, f"Command '{cmd}' not found in --help output"


class TestBlockmatchingCommand:
    def test_invokes_wrapper(self, tmp_path) -> None:
        ref = tmp_path / "ref.nii"
        flo = tmp_path / "flo.nii"
        ref.touch()
        flo.touch()
        with patch("blockmatchingw.commands.blockmatching._blockmatching") as mock_bm:
            result = runner.invoke(
                app,
                [
                    "blockmatching",
                    "--reference",
                    str(ref),
                    "--floating",
                    str(flo),
                    "--transformation-type",
                    "rigid3D",
                ],
            )
            assert result.exit_code == 0
            mock_bm.assert_called_once()
            call_kwargs = mock_bm.call_args
            assert call_kwargs[0][0] == ref
            assert call_kwargs[0][1] == flo
            assert call_kwargs[1]["transformation_type"] == "rigid3D"


class TestApplyTrsfCommand:
    def test_invokes_wrapper(self, tmp_path) -> None:
        flo = tmp_path / "flo.nii"
        flo.touch()
        with patch("blockmatchingw.commands.apply_trsf._apply_trsf") as mock_at:
            result = runner.invoke(
                app,
                [
                    "apply-trsf",
                    "--floating",
                    str(flo),
                    "--interpolation",
                    "nearest",
                ],
            )
            assert result.exit_code == 0
            mock_at.assert_called_once()
            assert mock_at.call_args[0][0] == flo
            assert mock_at.call_args[1]["interpolation"] == "nearest"


class TestInstallCommand:
    def test_platform_flag(self) -> None:
        with patch(
            "blockmatchingw.commands.install.get_platform", return_value="macos-arm64"
        ):
            result = runner.invoke(app, ["install", "--platform"])
            assert result.exit_code == 0

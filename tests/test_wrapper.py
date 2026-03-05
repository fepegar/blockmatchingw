"""Tests for the wrapper module."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from blockmatchingw.wrapper import (
    _get_path,
    _read_stream,
    _run_with_logging,
    apply_trsf,
    blockmatching,
    run,
)


class TestGetPath:
    def test_returns_path_when_found(self) -> None:
        with patch("blockmatchingw.wrapper._find", return_value=Path("/usr/bin/tool")):
            result = _get_path("tool")
        assert result == Path("/usr/bin/tool")

    def test_raises_when_not_found(self) -> None:
        with patch("blockmatchingw.wrapper._find", return_value=None):
            with pytest.raises(FileNotFoundError, match="tool not found"):
                _get_path("tool")

    def test_error_message_includes_install_hint(self) -> None:
        with patch("blockmatchingw.wrapper._find", return_value=None):
            with pytest.raises(FileNotFoundError, match="blockmatchingw install"):
                _get_path("blockmatching")


class TestReadStream:
    def test_reads_stdout_lines(self) -> None:
        mock_logger = Mock()
        stream = iter(["line 1\n", "line 2\n"])
        _read_stream(stream, is_stderr=False, tool_logger=mock_logger)
        assert mock_logger.info.call_count == 2
        mock_logger.info.assert_any_call("line 1")
        mock_logger.info.assert_any_call("line 2")

    def test_reads_stderr_as_warnings(self) -> None:
        mock_logger = Mock()
        stream = iter(["warning msg\n"])
        _read_stream(stream, is_stderr=True, tool_logger=mock_logger)
        mock_logger.warning.assert_called_once_with("warning msg")

    def test_uses_default_logger_when_no_tool_logger(self) -> None:
        stream = iter(["test line\n"])
        with patch("blockmatchingw.wrapper.logger") as mock_logger:
            _read_stream(stream, is_stderr=False, tool_logger=None)
            mock_logger.info.assert_called_once_with("test line")


class TestRun:
    def test_calls_popen_with_correct_args(self) -> None:
        with (
            patch("blockmatchingw.wrapper._find", return_value=Path("/usr/bin/tool")),
            patch("blockmatchingw.wrapper.Popen") as mock_popen,
        ):
            mock_process = Mock()
            mock_process.stdout = iter([])
            mock_process.stderr = iter([])
            mock_process.wait.return_value = 0
            mock_process.__enter__ = Mock(return_value=mock_process)
            mock_process.__exit__ = Mock(return_value=False)
            mock_popen.return_value = mock_process

            run("tool", "-arg1", "val1", "-arg2", "val2")

            mock_popen.assert_called_once_with(
                ["/usr/bin/tool", "-arg1", "val1", "-arg2", "val2"],
                stdout=-1,
                stderr=-1,
                text=True,
                bufsize=1,
            )

    def test_strips_whitespace_from_args(self) -> None:
        with (
            patch("blockmatchingw.wrapper._find", return_value=Path("/usr/bin/tool")),
            patch("blockmatchingw.wrapper.Popen") as mock_popen,
        ):
            mock_process = Mock()
            mock_process.stdout = iter([])
            mock_process.stderr = iter([])
            mock_process.wait.return_value = 0
            mock_process.__enter__ = Mock(return_value=mock_process)
            mock_process.__exit__ = Mock(return_value=False)
            mock_popen.return_value = mock_process

            run("tool", "-ref\\\n", "image.nii.gz")

            cmd = mock_popen.call_args[0][0]
            assert cmd == ["/usr/bin/tool", "-ref", "image.nii.gz"]

    def test_filters_empty_args(self) -> None:
        with (
            patch("blockmatchingw.wrapper._find", return_value=Path("/usr/bin/tool")),
            patch("blockmatchingw.wrapper.Popen") as mock_popen,
        ):
            mock_process = Mock()
            mock_process.stdout = iter([])
            mock_process.stderr = iter([])
            mock_process.wait.return_value = 0
            mock_process.__enter__ = Mock(return_value=mock_process)
            mock_process.__exit__ = Mock(return_value=False)
            mock_popen.return_value = mock_process

            run("tool", "", "-ref", "", "img.nii")

            cmd = mock_popen.call_args[0][0]
            assert cmd == ["/usr/bin/tool", "-ref", "img.nii"]


class TestRunWithLogging:
    def test_builds_args_from_lines(self) -> None:
        with (
            patch("blockmatchingw.wrapper._find", return_value=Path("/usr/bin/bm")),
            patch("blockmatchingw.wrapper.run") as mock_run,
        ):
            _run_with_logging("blockmatching", "-ref img.nii \\", "-flo flo.nii \\")
            mock_run.assert_called_once()
            args = mock_run.call_args[0]
            assert args[0] == "blockmatching"
            assert "-ref" in args
            assert "img.nii" in args
            assert "-flo" in args
            assert "flo.nii" in args


class TestBlockmatching:
    def test_basic_call(self, temp_dir: Path) -> None:
        ref = temp_dir / "ref.nii"
        flo = temp_dir / "flo.nii"
        with patch("blockmatchingw.wrapper._run_with_logging") as mock_run:
            blockmatching(ref, flo)
            mock_run.assert_called_once()
            args = mock_run.call_args[0]
            assert args[0] == "blockmatching"
            lines = " ".join(args[1:])
            assert str(ref) in lines
            assert str(flo) in lines

    def test_with_result_and_transformation(self, temp_dir: Path) -> None:
        ref = temp_dir / "ref.nii"
        flo = temp_dir / "flo.nii"
        res = temp_dir / "res.nii"
        trsf = temp_dir / "trsf.txt"
        with patch("blockmatchingw.wrapper._run_with_logging") as mock_run:
            blockmatching(ref, flo, result=res, result_transformation=trsf)
            args = mock_run.call_args[0]
            lines = " ".join(args[1:])
            assert f"-res {res}" in lines
            assert f"-res-trsf {trsf}" in lines

    def test_transformation_type(self, temp_dir: Path) -> None:
        ref = temp_dir / "ref.nii"
        flo = temp_dir / "flo.nii"
        with patch("blockmatchingw.wrapper._run_with_logging") as mock_run:
            blockmatching(ref, flo, transformation_type="rigid3D")
            args = mock_run.call_args[0]
            lines = " ".join(args[1:])
            assert "-trsf-type rigid3D" in lines

    def test_pyramid_levels(self, temp_dir: Path) -> None:
        ref = temp_dir / "ref.nii"
        flo = temp_dir / "flo.nii"
        with patch("blockmatchingw.wrapper._run_with_logging") as mock_run:
            blockmatching(ref, flo, pyramid_lowest_level=1, pyramid_highest_level=5)
            args = mock_run.call_args[0]
            lines = " ".join(args[1:])
            assert "-py-ll 1" in lines
            assert "-py-hl 5" in lines

    def test_normalisation_true(self, temp_dir: Path) -> None:
        ref = temp_dir / "ref.nii"
        flo = temp_dir / "flo.nii"
        with patch("blockmatchingw.wrapper._run_with_logging") as mock_run:
            blockmatching(ref, flo, normalisation=True)
            args = mock_run.call_args[0]
            lines = " ".join(args[1:])
            assert "-normalisation" in lines

    def test_normalisation_false(self, temp_dir: Path) -> None:
        ref = temp_dir / "ref.nii"
        flo = temp_dir / "flo.nii"
        with patch("blockmatchingw.wrapper._run_with_logging") as mock_run:
            blockmatching(ref, flo, normalisation=False)
            args = mock_run.call_args[0]
            lines = " ".join(args[1:])
            assert "-no-normalisation" in lines

    def test_verbose_flag(self, temp_dir: Path) -> None:
        ref = temp_dir / "ref.nii"
        flo = temp_dir / "flo.nii"
        with patch("blockmatchingw.wrapper._run_with_logging") as mock_run:
            blockmatching(ref, flo, verbose=True)
            args = mock_run.call_args[0]
            lines = " ".join(args[1:])
            assert "-v" in lines

    def test_block_size(self, temp_dir: Path) -> None:
        ref = temp_dir / "ref.nii"
        flo = temp_dir / "flo.nii"
        with patch("blockmatchingw.wrapper._run_with_logging") as mock_run:
            blockmatching(ref, flo, block_size=(4, 4, 4))
            args = mock_run.call_args[0]
            lines = " ".join(args[1:])
            assert "-bl-size 4 4 4" in lines

    def test_estimator_and_lts(self, temp_dir: Path) -> None:
        ref = temp_dir / "ref.nii"
        flo = temp_dir / "flo.nii"
        with patch("blockmatchingw.wrapper._run_with_logging") as mock_run:
            blockmatching(ref, flo, estimator_type="wlts", lts_cut=0.5)
            args = mock_run.call_args[0]
            lines = " ".join(args[1:])
            assert "-es-type wlts" in lines
            assert "-lts-cut 0.5" in lines


class TestApplyTrsf:
    def test_basic_call(self, temp_dir: Path) -> None:
        flo = temp_dir / "flo.nii"
        with patch("blockmatchingw.wrapper._run_with_logging") as mock_run:
            apply_trsf(flo)
            mock_run.assert_called_once()
            args = mock_run.call_args[0]
            assert args[0] == "applyTrsf"
            lines = " ".join(args[1:])
            assert str(flo) in lines

    def test_with_transformation_and_reference(self, temp_dir: Path) -> None:
        flo = temp_dir / "flo.nii"
        ref = temp_dir / "ref.nii"
        trsf = temp_dir / "trsf.txt"
        res = temp_dir / "res.nii"
        with patch("blockmatchingw.wrapper._run_with_logging") as mock_run:
            apply_trsf(
                flo,
                result=res,
                transformation=trsf,
                reference=ref,
            )
            args = mock_run.call_args[0]
            lines = " ".join(args[1:])
            assert f"-res {res}" in lines
            assert f"-trsf {trsf}" in lines
            assert f"-ref {ref}" in lines

    def test_interpolation_modes(self, temp_dir: Path) -> None:
        flo = temp_dir / "flo.nii"
        with patch("blockmatchingw.wrapper._run_with_logging") as mock_run:
            apply_trsf(flo, nearest=True)
            args = mock_run.call_args[0]
            lines = " ".join(args[1:])
            assert "-nearest" in lines

    def test_resize_and_iso(self, temp_dir: Path) -> None:
        flo = temp_dir / "flo.nii"
        with patch("blockmatchingw.wrapper._run_with_logging") as mock_run:
            apply_trsf(flo, resize=True, isotropic_voxel=1.0)
            args = mock_run.call_args[0]
            lines = " ".join(args[1:])
            assert "-resize" in lines
            assert "-iso 1.0" in lines

    def test_parallel_options(self, temp_dir: Path) -> None:
        flo = temp_dir / "flo.nii"
        with patch("blockmatchingw.wrapper._run_with_logging") as mock_run:
            apply_trsf(flo, parallel=True, max_chunks=4)
            args = mock_run.call_args[0]
            lines = " ".join(args[1:])
            assert "-parallel" in lines
            assert "-max-chunks 4" in lines

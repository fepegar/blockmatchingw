---
icon: lucide/heart-pulse
---

# blockmatchingw

Pythonic wrapper for [Klab-BlockMatching](https://github.com/fepegar/Klab-BlockMatching),
providing a modern CLI and Python API for block matching-based image registration.

[Klab-BlockMatching](https://github.com/fepegar/Klab-BlockMatching) is a suite of
tools for block matching-based image registration developed by the
[MORPHEME team](https://team.inria.fr/morpheme/) at
[INRIA](https://www.inria.fr/).

---

## Features

- :material-console: **Modern CLI** — Typer-based CLI with descriptive option
  names for all 16 BlockMatching tools
- :material-language-python: **Python API** — Call registration tools directly
  from Python with typed arguments
- :material-file-tree: **Structured logging** — Loguru-based logging with
  tool output classification
- :material-download: **Easy installation** — Install via `pip` or `uv`, with
  automatic binary download

## Quick start

=== "CLI"

    ```shell
    pip install blockmatchingw
    blockmatchingw blockmatching \
      --reference ref.nii.gz \
      --floating flo.nii.gz \
      --result-transformation trsf.txt
    ```

=== "Python"

    ```python
    from blockmatchingw import blockmatching

    blockmatching(
        reference="ref.nii.gz",
        floating="flo.nii.gz",
        result_transformation="trsf.txt",
    )
    ```

!!! tip "Looking for BlockMatching binaries?"

    `blockmatchingw` expects BlockMatching binaries (e.g., `blockmatching`) to
    be available on your `PATH`. See [Installation](installation.md) for details.

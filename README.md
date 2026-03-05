# `blockmatchingw`

Pythonic wrapper for [Klab-BlockMatching](https://github.com/fepegar/Klab-BlockMatching),
providing a modern CLI and Python API for block matching-based image registration.

Klab-BlockMatching is a suite of tools for block matching-based image
registration, developed by the
[MORPHEME team](https://team.inria.fr/morpheme/) at
[INRIA](https://www.inria.fr/).

## Installation

```shell
pip install blockmatchingw
```

Or with [`uv`](https://docs.astral.sh/uv/):

```shell
uv pip install blockmatchingw
```

## CLI

```shell
blockmatchingw --help
```

### Block matching registration

```shell
blockmatchingw blockmatching \
  --reference ref.nii.gz \
  --floating flo.nii.gz \
  --result-transformation trsf.txt \
  --result result.nii.gz
```

### Apply transformation

```shell
blockmatchingw apply-trsf \
  --floating input.nii.gz \
  --result output.nii.gz \
  --transformation trsf.txt \
  --reference ref.nii.gz
```

### All subcommands

| Subcommand             | Description                                   |
|------------------------|-----------------------------------------------|
| `install`              | Download and install BlockMatching binaries    |
| `blockmatching`        | Block matching-based image registration       |
| `apply-trsf`           | Apply a transformation to an image            |
| `apply-trsf-to-points` | Apply a transformation to point sets          |
| `compose-trsf`         | Compose transformations                       |
| `copy-trsf`            | Copy and convert transformations              |
| `create-grid`          | Create a deformation grid                     |
| `create-trsf`          | Create a transformation                       |
| `crop-image`           | Crop an image                                 |
| `intermediary-trsf`    | Compute intermediary transformations          |
| `interpolate-images`   | Interpolate between images                    |
| `inv-trsf`             | Invert a transformation                       |
| `pointmatching`        | Point matching-based registration             |
| `build-pyramid-image`  | Build image pyramids                          |
| `print-image`          | Print image information                       |
| `print-trsf`           | Print transformation information              |
| `test-libio`           | Test I/O library                              |

## Python

```python
from blockmatchingw import blockmatching

blockmatching(
    reference="ref.nii.gz",
    floating="flo.nii.gz",
    result_transformation="trsf.txt",
    result="result.nii.gz",
)
```

For any binary, use the generic `run` function:

```python
from blockmatchingw import run

run("blockmatching", "-ref", "ref.nii.gz", "-flo", "flo.nii.gz")
```
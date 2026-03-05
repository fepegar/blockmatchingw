# Python API

`blockmatchingw` provides a typed Python API alongside its CLI.

## `blockmatching`

The `blockmatching` function runs block matching registration with full type
annotations.

```python
from blockmatchingw import blockmatching

blockmatching(
    reference="ref.nii.gz",
    floating="flo.nii.gz",
    result_transformation="trsf.txt",
    transformation_type="rigid",
)
```

## `run`

For any binary, use the generic `run` function with raw arguments:

```python
from blockmatchingw import run

# Block matching registration
run(
    "blockmatching",
    "-ref", "ref.nii.gz",
    "-flo", "flo.nii.gz",
    "-res-trsf", "trsf.txt",
)

# Apply transformation
run(
    "applyTrsf",
    "-flo", "input.nii.gz",
    "-res", "output.nii.gz",
    "-trsf", "trsf.txt",
    "-ref", "ref.nii.gz",
)

# Invert transformation
run(
    "invTrsf",
    "forward.trsf",
    "inverse.trsf",
)
```

## All wrapper functions

Every BlockMatching tool has a corresponding typed Python function:

| Function | Binary | Description |
|----------|--------|-------------|
| `blockmatching()` | `blockmatching` | Block matching-based registration |
| `apply_trsf()` | `applyTrsf` | Apply transformation to image |
| `apply_trsf_to_points()` | `applyTrsfToPoints` | Apply transformation to points |
| `compose_trsf()` | `composeTrsf` | Compose transformations |
| `copy_trsf()` | `copyTrsf` | Copy/convert transformations |
| `create_grid()` | `createGrid` | Create deformation grid |
| `create_trsf()` | `createTrsf` | Create transformation |
| `crop_image()` | `cropImage` | Crop image |
| `intermediary_trsf()` | `intermediaryTrsf` | Intermediary transformations |
| `interpolate_images()` | `interpolateImages` | Interpolate images |
| `inv_trsf()` | `invTrsf` | Invert transformation |
| `pointmatching()` | `pointmatching` | Point matching registration |
| `build_pyramid_image()` | `buildPyramidImage` | Build image pyramids |
| `print_image()` | `printImage` | Print image info |
| `print_trsf()` | `printTrsf` | Print transformation info |
| `test_libio()` | `test-libio` | Test I/O library |

## Logging

`blockmatchingw` uses [Loguru](https://github.com/Delgan/loguru) for structured
logging.

You can pass a custom logger to `run`:

```python
from loguru import logger
from blockmatchingw import run

my_logger = logger.bind(executable="blockmatching")
run("blockmatching", "-ref", "ref.nii.gz", "-flo", "flo.nii.gz", tool_logger=my_logger)
```

# CLI reference

`blockmatchingw` provides subcommands for all 16 BlockMatching tools. Option
names use descriptive English instead of the terse original flags.

```shell
blockmatchingw --help
```

!!! tip "Original help"

    Every subcommand supports `-h` to print the **original** BlockMatching help
    message, and `--help` for the `blockmatchingw` help.

## `install`

Download and install BlockMatching binaries for your platform.

```shell
blockmatchingw install
blockmatchingw install --output-dir /opt/blockmatching/bin
```

| Option | Short | Description |
|--------|-------|-------------|
| `--output-dir` | `-o` | Directory to install binaries into (default: `~/.local/bin`) |

## `blockmatching`

Block matching-based image registration.

```shell
blockmatchingw blockmatching \
  --reference ref.nii.gz \
  --floating flo.nii.gz \
  --result-transformation trsf.txt
```

Common options:

| Option | Description |
|--------|-------------|
| `--reference` | Reference (target/fixed) image |
| `--floating` | Floating (source/moving) image |
| `--result` | Resampled output image |
| `--result-transformation` | Output transformation |
| `--transformation-type` | Type of transformation (e.g., rigid, affine, vectorfield) |
| `--pyramid-lowest-level` | Lowest pyramid level |
| `--pyramid-highest-level` | Highest pyramid level |

## `apply-trsf`

Apply a transformation to an image.

```shell
blockmatchingw apply-trsf \
  --floating input.nii.gz \
  --result output.nii.gz \
  --transformation trsf.txt \
  --reference ref.nii.gz
```

## `apply-trsf-to-points`

Apply a transformation to a set of points.

```shell
blockmatchingw apply-trsf-to-points \
  points_in.txt points_out.txt \
  --transformation trsf.txt
```

## `compose-trsf`

Compose multiple transformations.

```shell
blockmatchingw compose-trsf \
  --result composed.trsf \
  --transformations trsf1.txt trsf2.txt
```

## `copy-trsf`

Copy and convert transformations.

```shell
blockmatchingw copy-trsf \
  input.trsf output.trsf \
  --transformation-type rigid
```

## `create-grid`

Create a deformation grid visualization.

```shell
blockmatchingw create-grid \
  grid.nii.gz \
  --template ref.nii.gz
```

## `create-trsf`

Create a transformation (identity, random, etc.).

```shell
blockmatchingw create-trsf \
  --result identity.trsf \
  --transformation-type rigid3D \
  --identity
```

## `crop-image`

Crop an image.

```shell
blockmatchingw crop-image \
  input.nii.gz output.nii.gz \
  --origin 10 10 10 \
  --dim 100 100 100
```

## `intermediary-trsf`

Compute intermediary transformations.

```shell
blockmatchingw intermediary-trsf \
  input.trsf output.trsf \
  --t 0.5
```

## `interpolate-images`

Interpolate between two images.

```shell
blockmatchingw interpolate-images \
  --floating img0.nii.gz \
  --reference img1.nii.gz \
  --result-format interp_%03d.nii.gz \
  --transformation trsf.txt \
  --nimages 10
```

## `inv-trsf`

Invert a transformation.

```shell
blockmatchingw inv-trsf \
  forward.trsf inverse.trsf \
  --template ref.nii.gz
```

## `pointmatching`

Point matching-based registration.

```shell
blockmatchingw pointmatching \
  --reference ref_points.txt \
  --floating flo_points.txt \
  --result-transformation trsf.txt
```

## `build-pyramid-image`

Build image pyramids.

```shell
blockmatchingw build-pyramid-image \
  input.nii.gz \
  --result-image-format pyramid_%d.nii.gz
```

## `print-image`

Print image information.

```shell
blockmatchingw print-image image.nii.gz
```

## `print-trsf`

Print transformation information.

```shell
blockmatchingw print-trsf transformation.trsf
```

## `test-libio`

Test I/O library.

```shell
blockmatchingw test-libio file.nii.gz
```

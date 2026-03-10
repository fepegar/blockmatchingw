# Installation

## Install blockmatchingw

=== "pip"

    ```shell
    pip install blockmatchingw
    ```

=== "uv"

    ```shell
    uv pip install blockmatchingw
    ```

=== "As a CLI tool"

    ```shell
    uv tool install blockmatchingw
    ```

## Install BlockMatching

`blockmatchingw` requires the BlockMatching binaries to be available on your
`PATH`. The easiest way is to use the built-in `install` command:

```shell
blockmatchingw install
```

This downloads the latest pre-built BlockMatching binaries for your platform
and places them in `~/.local/bin` by default.

To install to a custom directory:

```shell
blockmatchingw install --output-dir /opt/blockmatching/bin
```

Or from Python:

```python
from blockmatchingw import download_blockmatching

download_blockmatching()  # ~/.local/bin
download_blockmatching("/opt/blockmatching/bin")  # custom directory
```

!!! warning "Ensure the directory is on your `PATH`"

    If `~/.local/bin` is not already on your `PATH`, add it:

    ```shell
    export PATH="$HOME/.local/bin:$PATH"
    ```

    Add this line to your `~/.bashrc` or `~/.zshrc` to make it permanent.

!!! note "Supported platforms"

    BlockMatching provides pre-built binaries for:

    - **Linux** x86_64
    - **macOS** Apple Silicon (arm64)
    - **macOS** Intel (x86_64)

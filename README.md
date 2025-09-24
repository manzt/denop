# Deno

Distribution of [Deno](https://deno.com/) for PyPI.

## Installation

```bash
pip install deno
```

```bash
uv add deno
```

## Usage

### Command Line

You can invoke Deno CLI directly via `uv` or `pipx`:

```bash
uvx deno --version
```

```bash
pipx deno --version
```

### Python API

```python
import deno

# Get the path to the Deno executable
deno_bin = deno.find_deno_bin()
```

## Platform Support

This package provides Deno binaries for:
- macOS (`x86_64`, `arm64`)
- Linux (`x86_64`, `arm64`)
- Windows (`x86_64`)

The appropriate binary for your platform will be installed automatically.

## License

MIT

This repository redistributes official Deno binaries to make them easily installable via pip/uv/etc.

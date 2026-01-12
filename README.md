# Deno

[![PyPI](https://img.shields.io/pypi/v/deno.svg)](https://pypi.org/project/deno/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/deno.svg)](https://pypi.org/project/deno/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/deno.svg)](https://pypi.org/project/deno/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python distribution of [Deno](https://deno.com/) — a secure runtime for JavaScript and TypeScript.

## Why This Package?

This package provides official Deno binaries through PyPI, making it easy to:

- **Install Deno without manual downloads** - No need to run shell scripts or download binaries manually
- **Integrate with Python workflows** - Use Deno in Python scripts, notebooks, and applications
- **Simplify CI/CD pipelines** - Install Deno as a regular Python dependency
- **Ensure version consistency** - Pin Deno versions in your `requirements.txt` or `pyproject.toml`
- **Cross-platform compatibility** - Automatic platform detection and binary selection

## Installation

Using `pip`:

```bash
pip install deno
```

Using `uv`:

```bash
uv add deno
```

Using `poetry`:

```bash
poetry add deno
```

## Usage

### Command Line

Run Deno directly using `uvx` or `pipx`:

```bash
# Check Deno version
uvx deno --version

# Run a TypeScript file
uvx deno run https://deno.land/std/examples/welcome.ts

# Start the REPL
pipx run deno
```

### Python API

Use Deno in your Python scripts:

```python
import subprocess
import deno

# Get the Deno executable path
deno_bin = deno.find_deno_bin()

# Run a Deno script
result = subprocess.run(
    [deno_bin, "run", "--allow-net", "script.ts"],
    capture_output=True,
    text=True
)
print(result.stdout)

# Check Deno version programmatically
version = subprocess.run(
    [deno_bin, "--version"],
    capture_output=True,
    text=True
)
print(version.stdout)
```

### CI/CD Integration

**GitHub Actions:**

```yaml
- name: Install Deno via pip
  run: pip install deno

- name: Run Deno script
  run: deno run --allow-all script.ts
```

**GitLab CI:**

```yaml
test:
  script:
    - pip install deno
    - deno run --allow-all script.ts
```

## Features

- **Cross-platform binary distribution** - Supports macOS, Linux, and Windows
- **No system dependencies** - Self-contained binaries with no external requirements
- **Multiple package manager support** - Works with pip, uv, pipx, poetry, and more
- **Python API** - Programmatic access to the Deno executable path
- **Automatic updates** - Package versions track official Deno releases

## Platform Support

This package provides Deno binaries for:

- **macOS**: `x86_64` (Intel), `arm64` (Apple Silicon)
- **Linux**: `x86_64`, `arm64`
- **Windows**: `x86_64`

The appropriate binary for your platform will be installed automatically.

## Versioning

This package version corresponds to the Deno version it distributes. For example:
- `deno==2.6.4` provides Deno v2.6.4
- `deno==2.6.3` provides Deno v2.6.3

To install a specific Deno version:

```bash
pip install deno==2.6.4
```

## Troubleshooting

### Binary not found error

If you encounter `FileNotFoundError`, ensure the package is properly installed:

```bash
pip install --force-reinstall deno
```

### Permission errors on Unix/Linux

If you get permission errors, you may need to ensure your scripts directory is in your PATH:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Using with virtual environments

When using virtual environments, activate your environment before installing:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install deno
```

## Links

- [Deno Official Website](https://deno.com/)
- [Deno Documentation](https://docs.deno.com/)
- [Deno GitHub Repository](https://github.com/denoland/deno)
- [PyPI Package](https://pypi.org/project/deno/)

## Contributing

Contributions are welcome! This package automatically redistributes official Deno binaries. To report issues or suggest improvements:

1. Check existing issues at the GitHub repository
2. Open a new issue with a clear description
3. Submit pull requests for bug fixes or enhancements

## License

MIT

This repository redistributes official Deno binaries to make them easily installable via pip/uv/etc. The Deno runtime itself is licensed under the MIT License by the Deno authors.

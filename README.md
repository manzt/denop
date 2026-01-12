# Deno for Python

[![PyPI version](https://img.shields.io/pypi/v/deno.svg)](https://pypi.org/project/deno/)
[![PyPI downloads](https://img.shields.io/pypi/dm/deno.svg)](https://pypi.org/project/deno/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

The easiest way to install and use [Deno](https://deno.com/) — the modern JavaScript and TypeScript runtime — in your Python projects.

## What is Deno?

Deno is a secure runtime for JavaScript and TypeScript that's built on V8, Rust, and Tokio. It features: 

- 🔒 **Secure by default** - No file, network, or environment access unless explicitly enabled
- 🚀 **TypeScript support** - Built-in TypeScript compiler, no configuration needed
- 📦 **Modern module system** - Native ES modules with URL imports
- 🛠️ **Built-in tooling** - Includes formatter, linter, test runner, bundler, and more
- 🌐 **Web standard APIs** - Compatible with browser APIs like `fetch`, `WebSocket`, and `Web Workers`
- ⚡ **High performance** - V8 engine with Rust-powered I/O

## Installation

### Using pip

```bash
pip install deno
```

### Using uv (recommended)

```bash
uv add deno
```

### Using poetry

```bash
poetry add deno
```

## Usage

### Command Line

Run Deno directly using `uvx` or `pipx`:

```bash
# Check version
uvx deno --version

# Run a script
uvx deno run https://examples.deno.land/hello-world.ts

# Start a REPL
uvx deno
```

With `pipx`:

```bash
pipx run deno --version
```

After installing with pip, the `deno` command is available in your PATH: 

```bash
deno run --allow-net server.ts
```

### Python API

Use the Python API to integrate Deno into your Python applications:

```python
import deno
import subprocess

# Get the path to the Deno executable
deno_bin = deno.find_deno_bin()

# Run a Deno script from Python
result = subprocess.run(
    [deno_bin, "run", "--allow-net", "script.ts"],
    capture_output=True,
    text=True
)

print(result.stdout)
```

### Example: Running TypeScript from Python

```python
import deno
import subprocess
import tempfile
import os

# Create a temporary TypeScript file
ts_code = """
console.log("Hello from Deno!");
const data = { message: "TypeScript works!" };
console.log(JSON.stringify(data));
"""

with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
    f.write(ts_code)
    ts_file = f.name

try:
    # Execute with Deno
    result = subprocess.run(
        [deno.find_deno_bin(), "run", ts_file],
        capture_output=True,
        text=True
    )
    print(result.stdout)
finally:
    os.unlink(ts_file)
```

## Platform Support

This package provides official Deno binaries for: 

| Platform | Architectures |
|----------|--------------|
| 🍎 **macOS** | x86_64 (Intel), arm64 (Apple Silicon) |
| 🐧 **Linux** | x86_64 (amd64), arm64 (aarch64) |
| 🪟 **Windows** | x86_64 (64-bit) |

The appropriate binary for your platform is automatically downloaded and installed.

## Common Use Cases

### Running Deno Scripts in Python Projects

Integrate JavaScript/TypeScript functionality into your Python applications:

```python
import deno
import subprocess

def run_deno_script(script_path: str, *args):
    """Execute a Deno script with arguments."""
    result = subprocess.run(
        [deno.find_deno_bin(), "run", "--allow-all", script_path, *args],
        capture_output=True,
        text=True
    )
    return result.stdout

output = run_deno_script("./scripts/process-data.ts", "input.json")
```

### Using Deno as a Task Runner

Add Deno scripts to your Python project for tasks like: 
- Frontend asset building
- API mocking
- Data processing with TypeScript
- Testing web APIs

### CI/CD Integration

Install Deno in your CI/CD pipelines:

```yaml
# GitHub Actions example
- name: Install Deno via pip
  run: pip install deno

- name: Run Deno tests
  run: deno test --allow-all
```

## Why Use deno via PyPI?

- ✅ **Easy integration** - Install Deno alongside Python dependencies
- ✅ **Version pinning** - Lock Deno versions in `requirements.txt` or `pyproject.toml`
- ✅ **No manual downloads** - Automatic binary management
- ✅ **Cross-platform** - Works seamlessly across development and production environments
- ✅ **Python API** - Programmatic access to Deno from Python code

## Version Compatibility

The version of this package corresponds to the Deno version it distributes. For example:
- `deno==2.1.0` includes Deno v2.1.0
- `deno==2.0.0` includes Deno v2.0.0

Check the [Deno releases](https://github.com/denoland/deno/releases) for version details.

## Resources

- 📚 [Deno Documentation](https://docs.deno.com/)
- 🌐 [Deno Website](https://deno.com/)
- 💬 [Deno Discord](https://discord.gg/deno)
- 📦 [PyPI Package](https://pypi.org/project/deno/)
- 🐙 [GitHub Repository](https://github.com/denoland/deno_pypi)
- 🦕 [Deno on GitHub](https://github.com/denoland/deno)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT

This repository redistributes official [Deno](https://deno.com/) binaries under the MIT license to make them easily installable via pip, uv, poetry, and other Python package managers.

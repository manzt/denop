```sh
scripts/build.sh # build all the distributions under ./dist
uvx --from dist/deno-2.3.5-py3-none-macosx_11_0_arm64.whl deno --version
# deno 2.3.5 (stable, release, aarch64-apple-darwin)
# v8 13.7.152.6-rusty
# typescript 5.8.3
```

```py
$ uv run --with dist/deno-2.3.5-py3-none-macosx_11_0_arm64.whl python
# Python 3.13.3 (main, May 30 2025, 05:45:55) [Clang 20.1.4 ] on darwin
# Type "help", "copyright", "credits" or "license" for more information.
# >>> import deno
# >>> deno.find_deno_bin()
# '/Users/manzt/.cache/uv/archive-v0/BykgqI7nUKj0T27s79pu3/bin/deno'
# >>>
```

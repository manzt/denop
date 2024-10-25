# Build the main
uv build --sdist

# Build the wheels
for zip in \
    "deno-aarch64-apple-darwin.zip" \
    "deno-aarch64-unknown-linux-gnu.zip" \
    "deno-x86_64-apple-darwin.zip" \
    "deno-x86_64-pc-windows-msvc.zip" \
    "deno-x86_64-unknown-linux-gnu.zip"
do
    # Set the target binary
    DENO_ARCHIVE_TARGET=$zip uv build --wheel
done

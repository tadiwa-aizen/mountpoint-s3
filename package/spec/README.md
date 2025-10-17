# Mountpoint-S3 Package Spec

This directory contains the packaging specifications and tools for building Mountpoint-S3 RPM packages.

## Contents

- `generate_spec.py` - Python script to generate distribution-specific RPM spec files
- `templates/` - Jinja2 template files for different distributions
- `pyproject.toml` - Python configuration

## How it Works

The `generate_spec.py` script creates RPM spec files by:

1. **Extracting versions** from project files:
   - Package version from `mountpoint-s3/Cargo.toml`
   - Rust toolchain version from `rust-toolchain.toml`
   - Git submodule versions for bundled libraries

2. **Rendering templates** using the extracted version data

3. **Outputting** a complete `.spec` file ready for `rpmbuild`

## Usage

Generate a spec file for a target distribution:
```bash
python generate_spec.py <build_target>
```

Examples:
```bash
# Generate amzn2023.spec from templates/amzn2023.spec.template
python generate_spec.py amzn2023

# Use custom template and output file
python generate_spec.py amzn2023 --template custom.spec.template --output my-package.spec
```

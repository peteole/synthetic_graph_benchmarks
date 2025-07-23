# PyPI Publishing Guide

This guide explains how to build and publish the `synthetic-graph-benchmarks` package to PyPI.

## Prerequisites

1. Install build tools:
```bash
pip install build twine
```

2. Ensure you have PyPI credentials configured:
   - Create account on [PyPI](https://pypi.org/) and [TestPyPI](https://test.pypi.org/)
   - Generate API tokens for both
   - Configure in `~/.pypirc` or use environment variables

## Building the Package

1. Clean previous builds:
```bash
rm -rf build/ dist/ *.egg-info/
```

2. Build the package:
```bash
python -m build
```

This creates both source distribution (.tar.gz) and wheel (.whl) files in the `dist/` directory.

## Testing the Build

1. Install locally to test:
```bash
pip install dist/synthetic_graph_benchmarks-*.whl
```

2. Run basic tests:
```bash
python -c "import synthetic_graph_benchmarks; print(synthetic_graph_benchmarks.__version__)"
```

## Publishing to TestPyPI (Recommended First)

1. Upload to TestPyPI:
```bash
python -m twine upload --repository testpypi dist/*
```

2. Test installation from TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ synthetic-graph-benchmarks
```

## Publishing to PyPI

1. Upload to PyPI:
```bash
python -m twine upload dist/*
```

2. Verify the package is available:
```bash
pip install synthetic-graph-benchmarks
```

## Version Management

Before each release:

1. Update version in `pyproject.toml`
2. Update version in `src/synthetic_graph_benchmarks/__init__.py`
3. Update CHANGELOG if you have one
4. Create a git tag:
```bash
git tag v0.1.0
git push origin v0.1.0
```

## Automated Publishing with GitHub Actions

Consider setting up GitHub Actions for automated publishing. Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## Security Notes

- Never commit API tokens to version control
- Use GitHub Secrets for automated publishing
- Consider using trusted publishing (OIDC) for better security

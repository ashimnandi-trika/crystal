# Publishing Crystal to PyPI

## One-Time Setup

### 1. Create PyPI Account
Go to https://pypi.org/account/register/ and create an account.

### 2. Generate API Token
1. Go to https://pypi.org/manage/account/token/
2. Create a new token with "Entire account" scope
3. Copy the token (starts with `pypi-`)

### 3. Configure twine
```bash
# Option A: Use environment variable
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE

# Option B: Create ~/.pypirc file
cat > ~/.pypirc << EOF
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE
EOF
```

## Publishing

### From the crystal-code directory:
```bash
cd /app/project-crystal/crystal-code

# 1. Clean previous builds
rm -rf dist/ build/ *.egg-info src/*.egg-info

# 2. Build the package
python -m build

# 3. Verify the package
twine check dist/*

# 4. Upload to PyPI
twine upload dist/*
```

### Verify it works:
```bash
pip install crystal-code
crystal --help
```

## Test PyPI (Optional - test first)
```bash
# Upload to test PyPI first
twine upload --repository testpypi dist/*

# Install from test PyPI
pip install --index-url https://test.pypi.org/simple/ crystal-code
```

## Updating (future releases)
1. Update version in `src/crystal_guard/__init__.py`
2. Update version in `pyproject.toml`
3. Run `python -m build && twine upload dist/*`

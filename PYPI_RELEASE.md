# 🚀 PyPI Release Instructions for WriteGuard v0.0.2

### 1. Prepare Environment
```bash
pip install setuptools wheel twine
```

### 2. Ensure `setup.py` is in root project dir (`WriteGuard/`)

### 3. Build Package
```bash
python setup.py sdist bdist_wheel
```

### 4. Check Build
```bash
twine check dist/*
```

### 5. Upload to Test PyPI
```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

### 6. Upload to PyPI
```bash
twine upload dist/*
```

### 7. Install to Verify
```bash
pip install writeguard==0.0.2
```

---

📦 Make sure your `__init__.py` and all modules are correctly included inside `app/v0.0.2/`

✍️ Author: Terry Simmons
🔗 License: MIT
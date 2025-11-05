# doxygen_to_md

[![Lint](https://github.com/<OWNER>/<REPO>/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/<OWNER>/<REPO>/actions/workflows/python-package.yml)

This project translates XML output from Doxygen into Markdown documentation source files for static website generation.

Quick start

Create a virtual environment and run tests:

```powershell
cd "D:\Documents\Python Scripts\doxygen_to_md"
python -m venv .venv; .\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e .
python -m pip install -r requirements-dev.txt
pytest -q
```

Note: Replace <OWNER>/<REPO> in the badge URL above with your GitHub username and repository name so the badge points to your repository's workflow.
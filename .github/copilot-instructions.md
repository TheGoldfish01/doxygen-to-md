# doxygen_to_md - AI Coding Guidelines

## Purpose

This file gives repository-specific guidance for GitHub Copilot (and other AI coding assistants) so suggestions are aligned with project goals, style, and verification expectations.

## Project overview

- Package name: `doxygen-to-md` (distribution name `doxygen-to-md`)
- Python package path: `src/doxygen_to_md`
- Tests: `tests/` (pytest)
- Build: PEP 517/518 using `pyproject.toml` + setuptools
- Supported Python: >= 3.8

## Primary goals for Copilot suggestions

- Implement features that convert Doxygen-style comments to Markdown with correct handling of tags like `@param`, `@return`, `@brief`, and code blocks.
- Produce well-typed, well-documented functions (use type hints and docstrings following Google or NumPy style). Keep docstrings concise and include examples where useful.
- Provide small, focused unit tests for each new behavior (pytest). New feature = at least one unit test covering the happy path, and one edge case where applicable.
- Keep changes minimal and safe: prefer adding small helper functions and tests rather than large sweeping edits.

## Coding conventions & rules

- Use type hints for public functions and internal helpers when helpful.
- Follow existing project layout: put runtime code under `src/doxygen_to_md` and tests under `tests`.
- Avoid changing external project metadata (license, package name) without explicit instruction.
- Maintain backwards compatibility for the public API in `src/doxygen_to_md/__init__.py` (the `convert` function and `__version__`). If bumping `__version__`, also update `pyproject.toml` when releasing.
- Add new dependencies only when necessary. If a dependency is proposed, add it to `pyproject.toml` and document why; prefer stdlib first.
- Keep CLI behavior stable: CLI entrypoint is `src/doxygen_to_md/cli.py` — it reads from file or stdin and prints Markdown.

## Testing and QA expectations

- Every functional change should include tests in `tests/` and pass with `pytest -q`.
- New code should have reasonable unit test coverage for core parsing logic and boundary cases (empty input, only comments, malformed tags).
- Tests should avoid network access and heavy IO. Use small in-memory examples.

## Pull request checklist for generated changes

- Add or update tests that cover the new behavior.
- Update `CHANGELOG.md` with a short entry under `## [Unreleased]` summarizing the change.
- Ensure the package builds (`python -m build`) locally if changing packaging metadata.
- If new CLI flags are added, update `README.md` usage examples.

## Suggested prompts and examples for Copilot

- "Implement a parser function that converts Doxygen `@param` tags into a Markdown table. Add unit tests for normal and missing parameter cases."
- "Refactor the `convert` function into smaller helpers: strip_comment_delimiters, parse_tags, to_markdown. Add tests for each helper."
- "Add handling of code blocks: detect @code/@endcode and convert to fenced markdown code blocks. Include tests."
- "Write a test that verifies that an empty string returns an empty string or an appropriate result."

## Example constraints to remind the assistant

- Keep each PR small and focused.
- Use the repo's existing Python version constraints (>=3.8).
- Do not change license text or remove files like `LICENSE` or `.github/workflows` unless asked.

```instructions
# doxygen_to_md - AI Coding Guidelines (PyANSYS-aligned)

## Purpose

This file gives repository-specific guidance for GitHub Copilot (and other AI coding assistants) so suggestions are aligned with project goals, PyANSYS development guidelines, and verification expectations.

## Project overview

- Package name: `doxygen-to-md` (distribution name `doxygen-to-md`)
- Python package path: `src/doxygen_to_md`
- Tests: `tests/` (pytest)
- Build: PEP 517/518 using `pyproject.toml` + setuptools
- Supported Python: >= 3.8

## High-level PyANSYS development expectations

Follow the PyANSYS project conventions where applicable. Key expectations for contributors and for Copilot-generated suggestions:

- Consistent formatting and linting: use `black` for formatting, `ruff` (or `flake8`) for linting, and `isort` for imports. Prefer minimal formatting changes in PRs.
- Static typing: use type hints for public APIs and for helpers where they improve readability and correctness. Strive for meaningful but practical typing (avoid overcomplicating with exotic typing patterns).
- Docstrings and documentation: use NumPy or Google-style docstrings for public functions and methods, and write short examples when helpful. New features that affect user-facing behaviour should include documentation (module docstring or README update).
- Tests: every feature or bugfix must include focused pytest tests that exercise the behavior. Use fixtures for shared setup and parameterized tests for common variations.
- CI: GitHub Actions must run tests across supported Python versions and linting/formatting checks. PRs should pass CI before merging.
- Pre-commit: recommend adding a `pre-commit` configuration to run formatting and linting hooks locally. Copilot should suggest pre-commit-friendly edits (i.e., code that passes hooks).
- Releases: follow semantic versioning. When bumping `__version__`, also update `pyproject.toml` and add an entry in `CHANGELOG.md` under `## [Unreleased]` describing the change.

## Primary goals for Copilot suggestions

- Implement features that convert Doxygen-style comments to Markdown with correct handling of tags like `@param`, `@return`, `@brief`, `@code`/`@endcode`, and nested/inline tags.
- Produce well-typed, well-documented functions. Prefer concise, clear docstrings following the project's chosen style.
- Provide small, focused unit tests for each new behavior. New feature = at least one unit test covering the happy path and one edge case where applicable.
- Keep PRs small and safe: prefer adding small helper functions and tests rather than large sweeping edits.

## Coding conventions & rules (Practical checklist)

- Keep public API stable: changes to `src/doxygen_to_md/__init__.py` (notably `convert` and `__version__`) are breaking and should be done deliberately.
- Add new dependencies only when necessary; justify them in the PR and add to `pyproject.toml`.
- Ensure code passes `black --check` and `ruff` (or `flake8`) locally and in CI.
- Write type hints for function signatures and returns. Use `typing` primitives and keep annotations readable.
- Prefer small helper functions with unit tests. Avoid long monolithic functions without tests.

## Testing and QA expectations

- Every functional change should include tests under `tests/` and pass with `pytest -q`.
- Tests should not require network access and should be fast. Use parametrized tests and fixtures to cover edge cases.
- Aim for meaningful assertions rather than implementation-based checks (test behavior not internal structure).

## Pull request checklist for generated changes (PyANSYS-aligned)

- Add or update tests that cover the new behavior.
- Run formatting and linting (e.g., `black`, `isort`, `ruff`) and ensure CI passes.
- Update `CHANGELOG.md` under `## [Unreleased]` with a short summary.
- If a public API changed, update `__version__` and document migration notes in the changelog and PR description.
- If packaging metadata is modified, ensure `pyproject.toml` builds (`python -m build`).
- Add or update documentation (README or module docstring) if CLI or API changed.

## Suggested prompts and examples for Copilot

- "Implement a parser function that converts Doxygen `@param` tags into a Markdown table. Add unit tests for normal and missing parameter cases. Make sure the code passes `black` and `ruff`."
- "Refactor `convert` into helpers: strip_comment_delimiters, parse_tags, to_markdown. Add tests for each helper and update `__init__.py` exports."
- "Add handling of `@code`/`@endcode` blocks converting to fenced markdown code blocks; include tests for language hints and nested tags."
- "Add a `pre-commit` config and update README with local development steps; include tests for the new behavior."

## Where to look before coding

- `src/doxygen_to_md/__init__.py` — public API and placeholder `convert` implementation.
- `src/doxygen_to_md/cli.py` — CLI behavior and usage.
- `tests/test_basic.py` — example of expected test structure.
- `pyproject.toml` — packaging metadata and Python version.
- `.github/workflows/python-package.yml` — CI expectations and matrix.

## Practical development snippets (for humans / Copilot to reference)

Local dev (PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e .[test]
python -m pip install -r requirements-dev.txt
pytest -q
black --check .
ruff check .
```

Add a test example template for new features:

```python
def test_new_feature():
	input_text = """/**\n * @brief Example.\n */"""
	out = convert(input_text)
	assert "Example" in out
```

## If you (Copilot) are unsure

- Prefer creating a small test and an implementation that satisfies the test.
- When suggesting dependency changes, explain why and add them to `pyproject.toml`.
- If unsure about public API changes, open an issue and propose alternatives rather than making breaking changes.

## Contact points (for humans reviewing Copilot output)

- Verify tests and linters run on GitHub Actions (`.github/workflows/python-package.yml`).
- Confirm changelog and version updates for release PRs.

Thank you — use this as a checklist for generating changes and PRs in this repository.

```

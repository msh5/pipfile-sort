<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD041 -->

<h1 align="center">
  pipfile-sort
</h1>

<div align="center">
  <strong>
    Sort package dependency lists in Pipfile.
  </strong>
  <br/>
  <br/>
  <a href="https://badge.fury.io/py/pipfile-sort"><img src="https://badge.fury.io/py/pipfile-sort.svg" alt="PyPI version" height="18"></a>
</div>

## Installation

```shell
pip install pipfile-sort
```

## Usage

```shell
# Pipfile-sort targets Pipfile on current directory,
# so need to move to the directory where Pipfile exists.
cd /path/to/pipfile/dir

# Rewrite Pipfile as the package lists are sorted.
pipfile-sort
```

## Pre-commit Hook

This package can be used as a [pre-commit](https://pre-commit.com/) hook.

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
- repo: https://github.com/msh5/pipfile-sort
  rev: v0.2.2  # Use the latest version
  hooks:
  - id: pipfile-sort
```

The hook will automatically sort your Pipfile when you commit changes.

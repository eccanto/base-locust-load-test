# Performance testing using Locust with Python

![](https://img.shields.io/badge/-Linux-grey?logo=linux)
![](https://img.shields.io/badge/license-MIT-green)
![](https://img.shields.io/github/stars/eccanto)

This project is an example of the different types of performance tests that are described in
[Performance testing summary](https://github.com/eccanto/base-performance-testing-documentation) using Locust and
Docker compose.

# Table of contents

* [Get started](#get-started)
  * [Requirements](#requirements)
  * [Configuration](#configuration)
  * [Run performance testing](#run-performance-testing)
    * [Implementation of "Case 1: Load testing"](#implementation-of-case-1-load-testing)
    * [Implementation of "case 2: Stress testing"](#implementation-of-case-2-stress-testing)
    * [Implementation of "Case 3: Soak testing"](#implementation-of-case-3-soak-testing)
    * [Implementation of "Case 4: Spike testing"](#implementation-of-case-4-spike-testing)
  * [Clean environment](#crean-environment)
* [Developers](#developers)
  * [Set up the Git Hooks custom directory](#set-up-the-git-hooks-custom-directory)
  * [Static code analysis tools](#static-code-analysis-tools)
    * [Python static code analysis tools](#python-static-code-analysis-tools)
    * [Run manually](#run-manually)
* [License](#license)

# Get Started

## Requirements

- [Docker +24.0.7](https://docs.docker.com/engine/install/ubuntu/)
- [Docker compose +2.21.0](https://docs.docker.com/compose/install/linux/)

## Configuration

Setup environment (start `mockoon` server) using docker compose:

```bash
docker compose --profile env up --detach
```

## Run performance testing

The following sections describe how to set up the execution environment, but do not start the test, for this you must
go to http://localhost:8089/, wait until all `10 workers` are connected and click on "**Start swarming**" button.

![Start swarming](./docs/videos/start_swarming.gif)

### Implementation of "Case 1: Load testing"

#### Run

Set `LOCUST_FILE=tests/load.py` in `.env` file:

```bash
sed -i 's/\(LOCUST_FILE=\).\+/\1tests\/load.py/' .env
```

Run load testing with `10` runners:

```bash
docker compose --profile test up --scale worker=10
```

#### Result

![Load testing result](./docs/images/locust-report-load-testing.png)

### Implementation of "Case 2: Stress testing"

#### Run

Set `LOCUST_FILE=tests/stress.py` in `.env` file:

```bash
sed -i 's/\(LOCUST_FILE=\).\+/\1tests\/stress.py/' .env
```

Run stress testing with `10` runners:

```bash
docker compose --profile test up --scale worker=10
```

#### Result

![Stress testing result](./docs/images/locust-report-stress-testing.png)

### Implementation of "Case 3: Soak testing"

#### Run

Set `LOCUST_FILE=tests/soak.py` in `.env` file:

```bash
sed -i 's/\(LOCUST_FILE=\).\+/\1tests\/soak.py/' .env
```

Run soak testing with `10` runners:

```bash
docker compose --profile test up --scale worker=10
```

#### Result

![Soak testing result](./docs/images/locust-report-soak-testing.png)

### Implementation of "Case 4: Spike testing"

#### Run

Set `LOCUST_FILE=tests/spike.py` in `.env` file:

```bash
sed -i 's/\(LOCUST_FILE=\).\+/\1tests\/spike.py/' .env
```

Run spike testing with `10` runners:

```bash
docker compose --profile test up --scale worker=10
```

#### Result

![Spike testing result](./docs/images/locust-report-spike-testing.png)

## Clean environment

```bash
docker compose --profile env --profile test down
```

# Developers

This project use [poetry](https://github.com/python-poetry/poetry) to run the static code analysis tools.

## Set up the Git Hooks custom directory

After cloning the repository run the following command in the repository root, this ensures that project static code
analysis tools (`tox -e check_code`) are run before each push into the repository to maintain the quality of the
project:

```bash
git config core.hooksPath .githooks
```

## Static code analysis tools

These are the static code analysis tools that will help us to follow good practices and style guides of our source code.
We will be using the following tools, which will be executed when generating a new push in the repository (git hooks).

### Python static code analysis tools

The tools used are:

* [ruff](https://github.com/astral-sh/ruff): An extremely fast Python linter and code formatter, written in Rust.

  Tools executed by Ruff:

  * [pycodestyle](https://github.com/PyCQA/pycodestyle): Pycodestyle is a tool to check your Python code against some
    of the style conventions in [PEP 8](https://peps.python.org/pep-0008/).
  * [ruff-format](https://github.com/astral-sh/ruff/blob/main/docs/formatter.md#black-compatibility): The formatter
    is designed to be a drop-in replacement for [Black](https://github.com/psf/black).
  * [flake8](https://github.com/PyCQA/flake8): Flake8 is a python tool that glues together pycodestyle, pyflakes,
    and third-party plugins to check the style and quality of some python code.
  * [pydocstyle](https://github.com/PyCQA/pydocstyle): Pydocstyle is a static analysis tool for checking compliance
    with [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).
  * [isort](https://pycqa.github.io/isort/): Python utility / library to sort imports alphabetically, and automatically
    separated into sections and by type.
  * [mccabe](https://github.com/PyCQA/mccabe): Complexity checker.
  * [bandit](https://github.com/PyCQA/bandit): Bandit is a tool designed to find common security issues.
  * [tryceratops](https://github.com/guilatrova/tryceratops): A linter to prevent exception handling antipatterns in
    Python.

* [prospector](https://github.com/PyCQA/prospector): Prospector is a tool to analyze Python code and output information
  about errors, potential problems, convention violations and complexity.

  Tools executed by Prospector:
  * [pylint](https://github.com/PyCQA/pylint): Pylint is a Python static code analysis tool which looks for programming
    errors, helps enforcing a coding standard, sniffs for code smells and offers simple refactoring suggestions.
  * [dodgy](https://github.com/landscapeio/dodgy): It is a series of simple regular expressions designed to detect
    things such as accidental SCM diff checkins, or passwords or secret keys hard coded into files.
  * [mypy](https://github.com/python/mypy): Mypy is an optional static type checker for Python.
  * [pyroma](https://github.com/regebro/pyroma): Pyroma is a product aimed at giving a rating of how well a Python
    project complies with the best practices of the Python packaging ecosystem, primarily PyPI, pip, Distribute etc,
    as well as a list of issues that could be improved.

### Run manually

```bash
bash .githooks/pre-push
```

# License

[MIT](./LICENSE)

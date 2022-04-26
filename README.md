# Deps

[![Tests](https://github.com/apoclyps/deps/actions/workflows/test.yml/badge.svg)](https://github.com/apoclyps/deps/actions/workflows/test.yml)
![pypi](https://img.shields.io/pypi/v/deps.svg)
![versions](https://img.shields.io/pypi/pyversions/deps.svg)

Simplify managing dependencies within an all-in-one TUI dashboard.

### Getting started with local development

To build and run the CLI on your host, you will need Python 3.9, pip, and virtualenv to build and run `review`.
If you wish to publish a PR with your changes, first create a fork on Github and clone that code.

```bash
$ gh repo clone apoclyps/deps
$ cd deps
$ python3 -m venv env
$ source env/bin/activate
(env)$ pip install -r requirements_dev.txt
(env)$ pip install -r requirements.txt
(env)$ python -m deps dashboard
```

If you wish to keep a copy of Deps on your host system, you can install and run it using:

```bash
python -m venv env
source env/bin/activate
python -m pip install -e .
deps -h
```

You can run the Deps within Docker:

```bash
docker-compose build cli && docker-compose run --rm cli python -m deps dashboard
```

To build an image and run that image with all of the necessary dependencies using the following commands:

```bash
docker-compose build cli
docker-compose run --rm cli python -m deps dashboard
```

### Testing

A test suite has been included to ensure Deps functions correctly.

To run the entire test suite with verbose output, run the following:

```bash
pytest -vvv
```

### Linting

To run individual linting steps:

```
docker-compose build test
docker-compose run --rm --no-deps test isort .
docker-compose run --rm --no-deps test black --line-length 119 --check .
docker-compose run --rm --no-deps test mypy .
docker-compose run --rm --no-deps test flake8 .
docker-compose run --rm --no-deps test pylint --rcfile=.pylintrc deps
docker-compose run --rm --no-deps test bandit deps
docker-compose run --rm --no-deps test vulture --min-confidence 90 deps
docker-compose run --rm --no-deps test codespell deps
docker-compose run --rm --no-deps test find . -name '*.py' -exec pyupgrade {} +
```

You can also set up ``pre-commit`` to run the linting steps automatically during the commit phase,
the pre-commit pipeline can be set up by running the following command on the project root:

```bash
pre-commit install
```

### Contributions

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

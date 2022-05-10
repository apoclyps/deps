# Deps

[![Tests](https://github.com/apoclyps/deps/actions/workflows/test.yml/badge.svg)](https://github.com/apoclyps/deps/actions/workflows/test.yml)
![pypi](https://img.shields.io/pypi/v/deps.svg)
![versions](https://img.shields.io/pypi/pyversions/deps.svg)

![](https://banners.beyondco.de/deps.png?theme=light&packageManager=pip+install&packageName=deps&pattern=architect&style=style_1&description=Improve+visibility+of+your+dependencies&md=1&showWatermark=1&fontSize=100px&images=https%3A%2F%2Flaravel.com%2Fimg%2Flogomark.min.svg)

Simplify managing dependencies within an all-in-one TUI dashboard.

## How to use deps

```bash
pip install deps

export GITHUB_USER="github-username"
export GITHUB_ORG="org"
export GITHUB_REPOSITORIES="repo_1,repo_2"
export GITHUB_TOKEN="secret"

# optional - export to svg
export DEPS_EXPORT_TO_SVG=false

deps dashboard
```

## Getting started with local development

To build and run the CLI on your host, you will need Python 3.9 or greater, pip, and virtualenv to build and run `deps`.
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

## Testing

A test suite has been included to ensure Deps functions correctly.

To run the entire test suite with verbose output, run the following:

```bash
make test
```

## Linting

To run individual linting steps:

```bash
make lint
```

You can also set up ``pre-commit`` to run the linting steps automatically during the commit phase,
the pre-commit pipeline can be set up by running the following command on the project root:

```bash
pre-commit install
```

To run all checks manually:

```bash
pre-commit run --all
```

## Contributions

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

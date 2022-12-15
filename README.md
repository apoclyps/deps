# Deps

[![Tests](https://github.com/apoclyps/deps/actions/workflows/test.yml/badge.svg)](https://github.com/apoclyps/deps/actions/workflows/test.yml)
![pypi](https://img.shields.io/pypi/v/deps.svg)
![versions](https://img.shields.io/pypi/pyversions/deps.svg)

![](https://banners.beyondco.de/deps.png?theme=light&packageManager=pip+install&packageName=deps&pattern=architect&style=style_1&description=Improve+visibility+of+your+dependencies&md=1&showWatermark=1&fontSize=100px&images=https%3A%2F%2Flaravel.com%2Fimg%2Flogomark.min.svg)

Simplify managing dependencies within an all-in-one TUI dashboard.

## How to use deps

You will need to create a GITHUB_TOKEN with permissions via [Github > Settings > Developer Settings](https://github.com/settings/tokens/new) with the `repo` permissions to read public/private repositories and and `admin:org` for `read:org` if you wish to access an organisation that is not public.

```bash
pip install deps

# your github username
export GITHUB_USER="user"
# an individual or an organisation in which the repository exists
export GITHUB_ORG="org"
# a comma separated list of repositories
export GITHUB_REPOSITORIES="repo_1,repo_2"
# your personal github token
export GITHUB_TOKEN="secret"

# optional - export to svg
export DEPS_EXPORT_TO_SVG=false

deps check
```

### Configuration

Deps supports both .ini and .env files. Deps always searches for configuration in this order:

* Environment variables;
* Repository: ini or .env file;
* Configuration Path
* Review Defaults

The following steps are used to provide the configuration using a `.env` or `.ini` file. The configuration can be read from within the module/repository (default location set by decouple) using the `.env` file or via a location specified by an environmental variable that points to a `.ini` file located in the root of the project or in a location specified by `PATH_TO_CONFIG`.

#### Using an `.env` file within the repository

```bash
cd /home/<your-user>/workspace/apoclyps/deps
touch .env

echo "GITHUB_ORG=apoclyps" >> .env
echo "GITHUB_REPOSITORIES=micropython-by-example" >> .env
python -m deps config
```

#### Using an `.ini` file within the repository

```bash
cd /home/<your-user>/workspace/apoclyps/deps
touch settings.ini
echo "[settings]\nGITHUB_ORG=apoclyps\nGITHUB_REPOSITORIES=micropython-by-example" >> settings.ini

python -m deps config
```

#### Providing a configuration path

If you wish to set the configuration path to use an `ini` or `.env` file when running the application, you can use the configuration of a specific file by supplying the path to the configuration like so:

```bash
cd /home/apoclyps/
touch settings.ini
echo "[settings]\nGITHUB_ORG=apoclyps\nGITHUB_REPOSITORIES=micropython-by-example" >> settings.ini

cd /home/<your-user>/workspace/apoclyps/deps
export DEPS_PATH_TO_CONFIG=/home/<your-user>/

python -m deps config
```

If at any time, you want to confirm your configuration reflects the file you have provided, you can use `deps config` to view what current configuration of Deps.

#### Configuring Layout


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
(env)$ python -m deps check
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
docker-compose build cli && docker-compose run --rm cli python -m deps check
```

To build an image and run that image with all of the necessary dependencies using the following commands:

```bash
docker-compose build cli
docker-compose run --rm cli python -m deps check
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

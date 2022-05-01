import click
from rich.console import Console

from deps.pipenv.view import DependenciesView

from ..version import __version__

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__, "-v", "--version", message="version %(version)s")
def cli() -> None:
    """Deps - A terminal UI Dashboard for monitoring code review requests.\n

    For feature requests or bug reports: https://github.com/apoclyps/deps/issues
    """


@cli.command(help="Visualize code review requests as a Dashboard")
def dashboard() -> None:
    """
    Command:\n
        deps dashboard
    """
    console = Console()
    DependenciesView(console=console).render()


def main() -> None:
    """Entry point to CLI"""
    cli()

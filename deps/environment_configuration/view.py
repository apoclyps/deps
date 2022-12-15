from dataclasses import dataclass

from rich.console import Console
from rich.table import Table

from deps import config


@dataclass
class EnvironmentConfigurationView:
    """Responsible for rendering a table of all dependencies grouped by service"""

    console: Console

    def __init__(self, console: Console) -> None:
        """Initialize the view"""

        self.console = console

    def render(self, show: bool) -> None:
        """Render the view"""

        configurations = [
            {
                "name": "GITHUB_TOKEN",
                "value": config.GITHUB_TOKEN if show else "".join("*" for _ in range(len(config.GITHUB_TOKEN))),
            },
            {"name": "GITHUB_USER", "value": config.GITHUB_USER},
            {"name": "GITHUB_URL", "value": config.GITHUB_URL},
            {
                "name": "DEPS_PATH_TO_CONFIG",
                "value": f"{config.DEPS_PATH_TO_CONFIG}",
            },
            {
                "name": "GITHUB_DEFAULT_PAGE_SIZE",
                "value": f"{config.GITHUB_DEFAULT_PAGE_SIZE}",
            },
            {
                "name": "EXTERNAL_SERVICE_MAXIMUM_REQUEST_ATTEMPTS",
                "value": f"{config.EXTERNAL_SERVICE_MAXIMUM_REQUEST_ATTEMPTS}",
            },
            {
                "name": "EXTERNAL_SERVICE_WAIT_IN_MS_BETWEEN_REQUESTS",
                "value": f"{config.EXTERNAL_SERVICE_WAIT_IN_MS_BETWEEN_REQUESTS}",
            },
            {"name": "DEPS_EXPORT_TO_SVG", "value": f"{config.DEPS_EXPORT_TO_SVG}"},
            {
                "name": "GITHUB_REPOSITORIES",
                "value": ", ".join(config.GITHUB_REPOSITORIES),
            },
        ]

        table = Table()
        table.add_column("Name", style="white", no_wrap=True)
        table.add_column("Value", style="cyan")

        for configuration in configurations:
            table.add_row(configuration["name"], configuration["value"])

        self.console.print(table)

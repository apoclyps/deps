from dataclasses import dataclass
from typing import Any

from rich.console import Console
from rich.table import Table

from deps.config import GITHUB_REPOSITORIES
from deps.pipenv.resolver import DependenciesResolver


@dataclass
class DependenciesView:
    """Responsible for rendering a table of all dependencies grouped by service"""

    console: Console
    used_versions_by_service: dict
    resolver: DependenciesResolver

    def __init__(self, console: Console) -> None:
        """Initialize the view"""
        self.used_versions_by_service = {}
        self.console = console
        self.resolver = DependenciesResolver()

    def render(self) -> None:
        """Render the view"""
        for repo in GITHUB_REPOSITORIES:
            file_dependencies: str = self.resolver.retrieve_file(repo=repo)

            used_versions_by_service: dict = self.resolver.compare_package_versions(repo=repo, lines=file_dependencies)
            if used_versions_by_service:
                self.used_versions_by_service = self.used_versions_by_service | used_versions_by_service

        if used_versions_by_service:
            for service_name, dependencies in used_versions_by_service.items():
                table = self.render_service_dependencies(
                    service_name=service_name,
                    dependencies=dependencies,
                )
                self.console.print(table)
        else:
            self.console.print("No dependencies found")

    def render_service_dependencies(self, service_name: str, dependencies: list[dict[Any, Any]]) -> Table:
        """Render the service dependencies"""
        table: Table = Table(title=service_name)

        table.add_column("Dependency Name", style="white", no_wrap=True)
        table.add_column("Current Version", style="red")
        table.add_column("Available Version", justify="right", style="green")

        for dependency in dependencies:
            current_version: str = dependency["current_version"]
            available_version: str = dependency["available_version"]

            # filter out versions that are identical
            if current_version != available_version:
                table.add_row(
                    dependency["dependency_name"],
                    current_version,
                    available_version,
                )

        return table

import os
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any

from rich.console import Console
from rich.table import Table

from deps.config import DEPS_EXPORT_TO_SVG, GITHUB_ORG, GITHUB_REPOSITORIES
from deps.pipenv.resolver import DependenciesResolver


@dataclass
class DependenciesView:
    """Responsible for rendering a table of all dependencies grouped by service"""

    console: Console
    used_versions_by_service: dict
    resolver: DependenciesResolver

    def __init__(self, console: Console) -> None:
        """Initialize the view"""
        console.record = DEPS_EXPORT_TO_SVG

        self.used_versions_by_service = {}
        self.console = console
        self.resolver = DependenciesResolver()

    def _retrieve(self, repo: str) -> dict:

        is_requirements: bool = False
        is_pipenv: bool = False
        is_poetry: bool = False

        requirements_urls: list[str] = [
            f"https://raw.githubusercontent.com/{GITHUB_ORG}/{repo}/main/requirements.txt",
            f"https://raw.githubusercontent.com/{GITHUB_ORG}/{repo}/master/requirements.txt",
        ]

        pipenv_urls: list[str] = [
            f"https://raw.githubusercontent.com/{GITHUB_ORG}/{repo}/main/Pipfile",
            f"https://raw.githubusercontent.com/{GITHUB_ORG}/{repo}/master/Pipfile",
        ]

        poetry_urls: list[str] = [
            f"https://raw.githubusercontent.com/{GITHUB_ORG}/{repo}/main/pyproject.toml",
            f"https://raw.githubusercontent.com/{GITHUB_ORG}/{repo}/master/pyproject.txt",
        ]

        file_dependencies: str | None = self.resolver.retrieve_file(repo=repo, urls=requirements_urls)
        is_requirements = bool(file_dependencies)

        if not is_requirements:
            file_dependencies = self.resolver.retrieve_file(repo=repo, urls=pipenv_urls)
            is_pipenv = bool(file_dependencies)

        if not is_pipenv:
            file_dependencies = self.resolver.retrieve_file(repo=repo, urls=poetry_urls)
            is_poetry = bool(file_dependencies)

        used_versions_by_service: dict = {}

        if is_requirements or is_pipenv:
            used_versions_by_service = self.resolver.compare_package_versions(repo=repo, lines=file_dependencies)
        elif is_poetry:
            used_versions_by_service = self.resolver.extract_package_versions(repo=repo, content=file_dependencies)

        return used_versions_by_service

    def render(self) -> None:
        """Render the view"""

        with ThreadPoolExecutor(max_workers=5) as executor:
            used_versions_by_services: list[dict] = list(executor.map(self._retrieve, GITHUB_REPOSITORIES))

        for used_versions_by_service in used_versions_by_services:
            if used_versions_by_service:
                self.used_versions_by_service = self.used_versions_by_service | used_versions_by_service

        if self.used_versions_by_service:
            for service_name, dependencies in self.used_versions_by_service.items():
                table = self.render_service_dependencies(
                    service_name=service_name,
                    dependencies=dependencies,
                )
                self.console.print(table, justify="center")
        else:
            self.console.print("No dependencies found")

        if DEPS_EXPORT_TO_SVG:
            self.console.save_svg("dependencies.svg", title="dependencies.py")

            webbrowser.open(f"file://{os.path.abspath('dependencies.svg')}")

    def render_service_dependencies(self, service_name: str, dependencies: list[dict[Any, Any]]) -> Table:
        """Render the service dependencies"""
        table: Table = Table(title=service_name, title_style="bold white", title_justify="center")

        table.add_column("Dependency Name", style="white", no_wrap=True, min_width=40)
        table.add_column("Current Version", justify="right", style="red", min_width=30)
        table.add_column("Available Version", justify="right", min_width=30)

        for dependency in dependencies:
            current_version: str = dependency["current_version"]
            available_version: str = dependency["available_version"]
            release_url: str = dependency["release_url"]

            # filter out versions that are identical
            if current_version != available_version:
                table.add_row(
                    dependency["dependency_name"],
                    current_version,
                    f"[link={release_url}][green]{available_version}[/green][/]",
                )

        return table

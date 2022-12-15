from dataclasses import dataclass
from re import match
from typing import Optional

import toml
from requests import get
from requests.auth import HTTPBasicAuth

from deps.config import GITHUB_TOKEN, GITHUB_USER
from deps.storage import cache

REGEX_PIPENV_DEPENDENCY_LINE = r"^(?P<name>.*)\s*\=\s*\"\=\=?(?P<version>.*)\"$"
REGEX_PIP_DEPENDENCY_LINE = r"^(?P<name>.*)==(?P<version>.*)$"


@dataclass
class DependenciesResolver:
    """Resolves package versions from Pipfile against PyPI"""

    versions_by_service: dict
    auth = None

    def __init__(self) -> None:
        """Initialize the resolver"""
        self.versions_by_service = {}
        self.auth = HTTPBasicAuth(GITHUB_USER, GITHUB_TOKEN)

    def retrieve_file(self, repo: str, urls: list[str]) -> str | None:
        """Retrieve the Pipfile from GitHub"""
        for url in urls:
            response = get(url=url, auth=self.auth, timeout=10)

            if response.status_code == 200:
                info: str = response.content.decode(encoding="UTF8")

                return info

        return None

    def compare_package_versions(self, repo: str, lines: str | None) -> dict:
        """Compare the package versions"""
        if not lines:
            return self.versions_by_service

        for line in lines.split("\n"):
            name: Optional[str] = None
            version: Optional[str] = None

            if pypi_match := match(REGEX_PIPENV_DEPENDENCY_LINE, line):
                name = pypi_match["name"].strip()
                version = pypi_match["version"].strip()
            elif pypi_match := match(REGEX_PIP_DEPENDENCY_LINE, line):
                name = pypi_match["name"].strip()
                version = pypi_match["version"].strip()
            else:
                # dependency does not match either pipfile or requirements.txt - skipping
                continue

            # replace invalid characters in the name
            name = name.replace("=", "")

            self._add_version_by_service(repo=repo, name=name, version=version)

        return self.versions_by_service

    def _add_version_by_service(self, repo: str, name: str, version: str) -> None:
        """Adds a package name and version to the versions used by that service"""
        if repo not in self.versions_by_service:
            self.versions_by_service[repo] = []

        info: dict[str, str] | None = cache.get(name=name)

        if info:
            available_version: str = info["available_version"]
            release_url: str = info["release_url"]

            self.versions_by_service[repo].append(
                {
                    "dependency_name": name,
                    "current_version": version,
                    "available_version": available_version,
                    "release_url": release_url,
                }
            )

    def extract_package_versions(self, repo: str, content: str | None) -> dict:
        """Compare the package versions"""
        if not content:
            return self.versions_by_service

        data: dict = toml.loads(content)
        poetry_sections: dict = data.get("tool", {}).get("poetry", {})

        for name, version in poetry_sections.get("dependencies", {}).items():
            version = version.replace("=", "")
            self._add_version_by_service(repo=repo, name=name, version=version)

        for name, version in poetry_sections.get("dev-dependencies", {}).items():
            version = version.replace("=", "")
            self._add_version_by_service(repo=repo, name=name, version=version)

        return self.versions_by_service

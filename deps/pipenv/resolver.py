from dataclasses import dataclass
from re import match
from typing import Optional

from requests import get
from requests.auth import HTTPBasicAuth

from deps.config import GITHUB_ORG, GITHUB_TOKEN, GITHUB_USER
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

    def retrieve_file(self, repo: str) -> str:
        """Retrieve the Pipfile from GitHub"""
        urls = [
            f"https://raw.githubusercontent.com/{GITHUB_ORG}/{repo}/main/Pipfile",
            f"https://raw.githubusercontent.com/{GITHUB_ORG}/{repo}/master/Pipfile",
            f"https://raw.githubusercontent.com/{GITHUB_ORG}/{repo}/main/requirements.txt",
            f"https://raw.githubusercontent.com/{GITHUB_ORG}/{repo}/master/requirements.txt",
        ]

        for url in urls:
            response = get(url=url, auth=self.auth)

            if response.status_code != 404:
                info: str = response.content.decode(encoding="UTF8")

                return info

        return ""

    def compare_package_versions(self, repo: str, lines: str) -> dict:
        """Compare the package versions"""
        if not lines:
            return {}

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

            if repo not in self.versions_by_service:
                self.versions_by_service[repo] = []

            info: dict[str, str] = cache.get(name=name)
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

        return self.versions_by_service

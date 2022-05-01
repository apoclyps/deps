from dataclasses import dataclass
from re import match

from requests import get
from requests.auth import HTTPBasicAuth

from deps.config import GITHUB_ORG, GITHUB_TOKEN, GITHUB_USER
from deps.storage import cache

REGEX_AVAILABLE_LINE = r"^Available\sversions:\s(?P<latest>[^,]*)"
REGEX_HEADER = r"\[.*\]"
REGEX_PACKAGE_HEADER = r"\[(?:dev-)?packages\]"
REGEX_PYPI_LINE = r"^(?P<name>.*)\s*\=\s*\"(?:==)?(?P<version>.*)\"$"


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
        ]

        for url in urls:
            response = get(url=url, auth=self.auth)

            if response.status_code != 404:
                return response.content.decode(encoding="UTF8")

        return ""

    def compare_package_versions(self, repo: str, lines: str) -> dict:
        """Compare the package versions"""
        reading_packages = False

        if not lines:
            return {}

        for line in lines.split("\n"):
            # Only worry about package sections
            if match(REGEX_HEADER, line):
                reading_packages = bool(match(REGEX_PACKAGE_HEADER, line))

            if not reading_packages:
                continue

            # Grab package name and pip version
            if pypi_match := match(REGEX_PYPI_LINE, line):
                name = pypi_match["name"].strip()
                version = pypi_match["version"].strip()

                if repo not in self.versions_by_service:
                    self.versions_by_service[repo] = []

                available_version: str = cache.get(name=name)
                self.versions_by_service[repo].append(
                    {
                        "dependency_name": name,
                        "current_version": version,
                        "available_version": available_version,
                    }
                )

        return self.versions_by_service

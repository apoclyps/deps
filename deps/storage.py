from dataclasses import dataclass

import requests


@dataclass
class PackageCache:
    """A cache of the latest versions of packages"""

    cache: dict[str, dict[str, str]]

    def __init__(self) -> None:
        """Initialize the cache"""
        self.cache: dict[str, str] = {}

    def retrieve(self, name: str) -> None:
        """Retrieve the latest version of a package from PyPI"""
        response = requests.get(f"https://pypi.org/pypi/{name}/json")

        if info := response.json()["info"]:
            self.cache[name] = {
                "available_version": str(info["version"]),
                "release_url": str(info["release_url"]),
            }

    def get(self, name: str) -> dict[str, str]:
        """Get the latest version of a package from the cache"""
        if name not in self.cache:
            self.retrieve(name)

        return self.cache[name]


cache: PackageCache = PackageCache()

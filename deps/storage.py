from dataclasses import dataclass
from http import HTTPStatus

import requests
from requests.exceptions import ConnectionError as HTTPConnectionError, HTTPError
from retrying import retry

from deps.config import EXTERNAL_SERVICE_MAXIMUM_REQUEST_ATTEMPTS, EXTERNAL_SERVICE_WAIT_IN_MS_BETWEEN_REQUESTS


def retry_if_connection_or_http_error(exception: Exception) -> bool:
    """Retries on connection and HTTP errors"""
    if isinstance(exception, (HTTPConnectionError, HTTPError)):
        return True

    return False


@dataclass
class PackageCache:
    """A cache of the latest versions of packages"""

    cache: dict[str, dict[str, str]]

    def __init__(self) -> None:
        """Initialize the cache"""
        self.cache: dict[str, str] = {}

    @retry(
        retry_on_exception=retry_if_connection_or_http_error,
        stop_max_attempt_number=EXTERNAL_SERVICE_MAXIMUM_REQUEST_ATTEMPTS,
        wait_exponential_multiplier=EXTERNAL_SERVICE_WAIT_IN_MS_BETWEEN_REQUESTS,
    )
    def retrieve(self, name: str) -> None:
        """Retrieve the latest version of a package from PyPI"""
        response = requests.get(f"https://pypi.org/pypi/{name}/json", timeout=10)

        if response.status_code not in (HTTPStatus.OK, HTTPStatus.NOT_FOUND):
            response.raise_for_status()

        if response.status_code != HTTPStatus.NOT_FOUND:
            if info := response.json().get("info"):
                self.cache[name] = {
                    "available_version": str(info["version"]),
                    "release_url": str(info["release_url"]),
                }

    def get(self, name: str) -> dict[str, str] | None:
        """Get the latest version of a package from the cache"""
        if name not in self.cache:
            self.retrieve(name)

        if name not in self.cache:
            return None

        return self.cache[name]


cache: PackageCache = PackageCache()

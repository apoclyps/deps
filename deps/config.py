from decouple import AutoConfig, Csv

config = AutoConfig()


# Github Config
GITHUB_DEFAULT_PAGE_SIZE = config("GITHUB_DEFAULT_PAGE_SIZE", cast=int, default=100)
GITHUB_ORG = config("GITHUB_ORG", cast=str)
GITHUB_REPOSITORIES = config("GITHUB_REPOSITORIES", cast=Csv(post_process=list[str], strip=" "))
GITHUB_TOKEN = config("GITHUB_TOKEN", cast=str)
GITHUB_URL = config("GITHUB_URL", cast=str, default="https://api.github.com")
GITHUB_USER = config("GITHUB_USER", cast=str)

# External Requests Config
EXTERNAL_SERVICE_MAXIMUM_REQUEST_ATTEMPTS = config("EXTERNAL_SERVICE_MAXIMUM_REQUEST_ATTEMPTS", cast=int, default=3)
EXTERNAL_SERVICE_WAIT_IN_MS_BETWEEN_REQUESTS = config(
    "EXTERNAL_SERVICE_WAIT_IN_MS_BETWEEN_REQUESTS", cast=int, default=250
)

# Deps Config
DEPS_EXPORT_TO_SVG = config("DEPS_EXPORT_TO_SVG", cast=bool, default=False)

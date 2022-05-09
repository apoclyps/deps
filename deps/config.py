from decouple import AutoConfig, Csv

config = AutoConfig()


# Github Config
GITHUB_DEFAULT_PAGE_SIZE = config("GITHUB_DEFAULT_PAGE_SIZE", cast=int, default=100)
GITHUB_ORG = config("GITHUB_ORG", cast=str)
GITHUB_REPOSITORIES = config("GITHUB_REPOSITORIES", cast=Csv())
GITHUB_TOKEN = config("GITHUB_TOKEN", cast=str)
GITHUB_URL = config("GITHUB_URL", cast=str, default="https://api.github.com")
GITHUB_USER = config("GITHUB_USER", cast=str)

# Deps Config
DEPS_EXPORT_TO_SVG = config("DEPS_EXPORT_TO_SVG", cast=bool, default=False)

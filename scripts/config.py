from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INFRA_REPO = PROJECT_ROOT


def get_app_repo(app_repo: str | None = None) -> Path:
    """
    Returns the application repository path.

    If app_repo is supplied, use it.
    Otherwise assume a sibling repository.
    """

    if app_repo:
        return Path(app_repo).resolve()

    return PROJECT_ROOT.parent / "devops-asset-inventory"
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INFRA_REPO = PROJECT_ROOT


def get_app_repo(app_repo: str | Path | None = None) -> Path:
    """
    Return the application repository.

    Priority:
        1. Explicit path supplied by caller.
        2. Jenkins workspace layout (application/)
        3. Local sibling repository (../devops-asset-inventory)
    """

    # Explicit path supplied
    if app_repo:
        return Path(app_repo).resolve()

    # Jenkins workspace
    jenkins_repo = PROJECT_ROOT / "application"
    if jenkins_repo.exists():
        return jenkins_repo.resolve()

    # Local development
    local_repo = PROJECT_ROOT.parent / "devops-asset-inventory"
    if local_repo.exists():
        return local_repo.resolve()

    raise FileNotFoundError(
        "Unable to locate application repository. "
        "Pass --app-repo or clone the application repository."
    )
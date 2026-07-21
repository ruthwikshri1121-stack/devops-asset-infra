import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INFRA_ROOT = PROJECT_ROOT


def load_registry():
    """
    Load registry configuration from images.json.
    """

    images_json = INFRA_ROOT / "images.json"

    if not images_json.exists():
        raise FileNotFoundError(f"{images_json} not found")

    with images_json.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if "registry" not in data:
        raise ValueError("Missing 'registry' section in images.json")

    return data["registry"]


def get_registry_url():
    """
    Return registry URL.
    """

    return load_registry().get("url", "").strip()


def get_repository():
    """
    Return repository name.
    """

    return load_registry().get("repository", "").strip()


def get_full_repository():
    """
    Return the complete repository path.
    """

    registry = load_registry()

    url = registry.get("url", "").strip()
    repo = registry.get("repository", "").strip()

    if url and repo:
        return f"{url}/{repo}"

    if url:
        return url

    if repo:
        return repo

    return ""
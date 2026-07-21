import json
import subprocess
from datetime import datetime
from pathlib import Path

from config import get_app_repo


def load_metadata(app_repo=None):

    app_repo = get_app_repo(app_repo)

    image_json = app_repo / "image.json"

    if not image_json.exists():
        raise FileNotFoundError(f"{image_json} not found")

    with image_json.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_metadata(metadata):

    required = [
        "image_name",
        "dockerfile",
        "build_context",
        "base_image",
        "base_image_version",
    ]

    for field in required:
        if field not in metadata:
            raise ValueError(f"Missing required field: {field}")


def _git(cmd, cwd):
    """
    Execute a git command and return its output.
    """

    return subprocess.check_output(
        cmd,
        cwd=cwd,
        text=True,
    ).strip()


def get_git_metadata(app_repo=None):

    app_repo = get_app_repo(app_repo)

    return {
        "commit": _git(["git", "rev-parse", "--short", "HEAD"], app_repo),
        "branch": _git(["git", "rev-parse", "--abbrev-ref", "HEAD"], app_repo),
        "author": _git(["git", "log", "-1", "--pretty=%an"], app_repo),
        "message": _git(["git", "log", "-1", "--pretty=%s"], app_repo),
    }


def get_build_metadata():

    return {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }


def get_full_metadata(app_repo=None):

    metadata = load_metadata(app_repo)

    validate_metadata(metadata)

    metadata.update(get_git_metadata(app_repo))

    metadata.update(get_build_metadata())

    return metadata
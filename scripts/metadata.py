import json
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
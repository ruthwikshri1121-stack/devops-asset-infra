import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INFRA_ROOT = PROJECT_ROOT


def load_registry():

    images_json = INFRA_ROOT / "images.json"

    with images_json.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return data["registry"]
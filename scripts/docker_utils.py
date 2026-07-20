import subprocess
from pathlib import Path
from registry import load_registry
from config import get_app_repo


def build_image(metadata, version):

    registry = load_registry()

    image_tag = (
        f"{registry['url']}/"
        f"{registry['repository']}/"
        f"{metadata['image_name']}:{version}"
    )

    app_repo = get_app_repo(app_repo)

    dockerfile = app_repo / metadata["dockerfile"]

    build_context = app_repo / metadata["build_context"]

    command = [
        "docker",
        "build",
        "-f",
        str(dockerfile),
        "-t",
        image_tag,
        str(build_context),
    ]

    print("\nExecuting Docker Build\n")

    print(" ".join(command))

    subprocess.run(command, check=True)

    print(f"\nImage built successfully: {image_tag}")
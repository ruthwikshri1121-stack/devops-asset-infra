import subprocess

from registry import load_registry
from config import get_app_repo


def build_image(metadata, version, app_repo=None):
    """
    Build the Docker image.

    Args:
        metadata (dict): Image metadata loaded from image.json.
        version (str): Generated image version.
        app_repo (str | None): Path to the application repository.
    """

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

    print("\n========== Docker Build ==========")
    print(f"Dockerfile   : {dockerfile}")
    print(f"Build Context: {build_context}")
    print(f"Image Tag    : {image_tag}")
    print()

    print("Executing:")
    print(" ".join(command))
    print()

    subprocess.run(command, check=True)

    print("\nDocker image built successfully!")
    print(f"Image: {image_tag}")
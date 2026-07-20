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

    registry_url = registry.get("url", "").strip()
    repository = registry.get("repository", "").strip()

    image_name = metadata["image_name"]

    if registry_url and repository:
        image_tag = f"{registry_url}/{repository}/{image_name}:{version}"
    elif registry_url:
        image_tag = f"{registry_url}/{image_name}:{version}"
    elif repository:
        image_tag = f"{repository}/{image_name}:{version}"
    else:
        image_tag = f"{image_name}:{version}"

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


def push_image(metadata, version):
    """
    Push the Docker image to the configured registry.
    """

    registry = load_registry()

    registry_url = registry.get("url", "").strip()
    repository = registry.get("repository", "").strip()

    image_name = metadata["image_name"]

    if registry_url and repository:
        image_tag = f"{registry_url}/{repository}/{image_name}:{version}"
    elif registry_url:
        image_tag = f"{registry_url}/{image_name}:{version}"
    elif repository:
        image_tag = f"{repository}/{image_name}:{version}"
    else:
        raise ValueError(
            "Registry URL and repository are empty. "
            "Cannot push image."
        )

    print("\n========== Docker Push ==========")
    print(f"Image: {image_tag}")
    print()

    command = [
        "docker",
        "push",
        image_tag,
    ]

    print("Executing:")
    print(" ".join(command))
    print()

    subprocess.run(command, check=True)

    print("\nDocker image pushed successfully!")
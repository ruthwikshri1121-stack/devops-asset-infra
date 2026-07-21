import subprocess

from registry import load_registry
from config import get_app_repo


def get_image_tag(metadata, version):
    """
    Construct the fully qualified Docker image tag.
    """

    registry = load_registry()

    registry_url = registry.get("url", "").strip()
    repository = registry.get("repository", "").strip()

    image_name = metadata["image_name"]

    if registry_url and repository:
        return f"{registry_url}/{repository}/{image_name}:{version}"

    if registry_url:
        return f"{registry_url}/{image_name}:{version}"

    if repository:
        return f"{repository}/{image_name}:{version}"

    return f"{image_name}:{version}"


def build_image(metadata, version, app_repo=None):
    """
    Build the Docker image.

    Args:
        metadata (dict): Image metadata loaded from image.json.
        version (str): Image version.
        app_repo (str |None): Application repository path.
    """

    image_tag = get_image_tag(metadata, version)

    app_repo = get_app_repo(app_repo)

    dockerfile = app_repo / metadata["dockerfile"]
    build_context = app_repo / metadata["build_context"]

    command = [
        "docker",
        "build",

        "--label", f"image.name={metadata['image_name']}",
        "--label", f"image.version={version}",
        "--label", f"git.commit={metadata.get('commit', '')}",
        "--label", f"git.branch={metadata.get('branch', '')}",
        "--label", f"git.author={metadata.get('author', '')}",
        "--label", f"build.timestamp={metadata.get('timestamp', '')}",

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

    return image_tag


def push_image(metadata, version):
    """
    Push the Docker image to the configured registry.
    """

    registry = load_registry()

    registry_url = registry.get("url", "").strip()
    repository = registry.get("repository", "").strip()

    if not registry_url and not repository:
        raise ValueError(
            "Registry URL and repository are empty. Cannot push image."
        )

    image_tag = get_image_tag(metadata, version)

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

    return image_tag
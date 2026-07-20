import argparse

from metadata import load_metadata, validate_metadata
from version import generate_version
from docker_utils import push_image


def main():

    parser = argparse.ArgumentParser(
        description="Push Docker image to registry"
    )

    parser.add_argument(
        "--app-repo",
        default=None,
        help="Path to application repository",
    )

    args = parser.parse_args()

    metadata = load_metadata(args.app_repo)

    validate_metadata(metadata)

    version = generate_version()

    push_image(metadata, version)


if __name__ == "__main__":
    main()
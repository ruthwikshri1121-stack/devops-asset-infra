import argparse

from metadata import load_metadata, validate_metadata
from version import generate_version
from docker_utils import build_image


def main():
    try:
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "--app-repo",
            help="Path to application repository",
            default=None,
        )

        args = parser.parse_args()

        metadata = load_metadata(args.app_repo)
        validate_metadata(metadata)

        version = generate_version()

        build_image(metadata, version, args.app_repo)

        print("Image build completed successfully.")

    except Exception as e:
        print(f"ERROR: {e}")
        raise


if __name__ == "__main__":
    main()
#!/usr/bin/env python3

"""
Version management utility.

Reads images.json, increments semantic version,
updates the file and returns the new version.
"""

import argparse
import json
from pathlib import Path


class VersionManager:

    def __init__(self, images_file: Path):

        self.images_file = Path(images_file)

        with self.images_file.open("r", encoding="utf-8") as fp:
            self.data = json.load(fp)

    def get_current_version(self, application):

        version = self.data["applications"][application].get("version", "")

        if not version:
            return "1.0.0"

        return version

    def increment_patch(self, version):

        major, minor, patch = version.split(".")

        return f"{major}.{minor}.{int(patch) + 1}"

    def increment_minor(self, version):

        major, minor, _ = version.split(".")

        return f"{major}.{int(minor) + 1}.0"

    def increment_major(self, version):

        major, _, _ = version.split(".")

        return f"{int(major) + 1}.0.0"

    def generate(self, application, level="patch"):

        current = self.get_current_version(application)

        if level == "major":
            return self.increment_major(current)

        if level == "minor":
            return self.increment_minor(current)

        return self.increment_patch(current)


def generate_version(images_file, application, level="patch"):
    """
    Generate the next semantic version without updating images.json.
    """

    manager = VersionManager(images_file)

    return manager.generate(application, level)


def main():

    parser = argparse.ArgumentParser(
        description="Generate semantic image version"
    )

    parser.add_argument(
        "--images",
        required=True,
        help="Path to images.json",
    )

    parser.add_argument(
        "--application",
        required=True,
        help="Application name",
    )

    parser.add_argument(
        "--level",
        default="patch",
        choices=["patch", "minor", "major"],
    )

    parser.add_argument(
        "--update",
        action="store_true",
        help="Persist the generated version into images.json",
    )

    args = parser.parse_args()

    version = generate_version(
        images_file=Path(args.images),
        application=args.application,
        level=args.level,
    )

    if args.update:
        save_version(
            images_file=Path(args.images),
            application=args.application,
            version=version,
        )

    print(version)


if __name__ == "__main__":
    main()
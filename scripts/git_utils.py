#!/usr/bin/env python3

"""
git_utils.py

Utility script for committing and pushing build metadata to GitHub.

Responsibilities:
- Configure Git identity
- Stage images.json
- Commit build metadata
- Push commit to GitHub

Example:

python scripts/git_utils.py \
    --images images.json \
    --version 1.0.2 \
    --username "Jenkins CI" \
    --email "jenkins@versa-demo.local" \
    --token <github_pat> \
    --repository ruthwikshri1121-stack/devops-asset-infra
"""

import argparse
import subprocess
import sys


# ---------------------------------------------------------
# Utility
# ---------------------------------------------------------

def run(command):
    """
    Execute a shell command.

    Raises RuntimeError if the command fails.
    """

    result = subprocess.run(
        command,
        shell=True,
        text=True,
        capture_output=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return result.stdout.strip()


# ---------------------------------------------------------
# Git Operations
# ---------------------------------------------------------

def configure_git(username, email):
    print("Configuring Git identity...")

    run(f'git config user.name "{username}"')
    run(f'git config user.email "{email}"')


def stage_changes(images_file):
    print(f"Staging {images_file}...")

    run(f"git add {images_file}")


def has_changes():
    """
    Returns True if staged changes exist.
    """

    result = subprocess.run(
        "git diff --cached --quiet",
        shell=True
    )

    return result.returncode != 0


def commit_changes(version):
    print("Creating commit...")

    message = f"ci: update devops-asset-inventory to {version}"

    run(f'git commit -m "{message}"')


def push_changes(token, repository):
    print("Pushing to GitHub...")

    remote = (
        f"https://ruthwikshri1121-stack:{token}"
        f"@github.com/{repository}.git"
    )

    run(f'git remote set-url origin "{remote}"')
    run("git push origin HEAD:main")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Commit and push build metadata."
    )

    parser.add_argument(
        "--images",
        required=True,
        help="images.json path"
    )

    parser.add_argument(
        "--version",
        required=True,
        help="Image version"
    )

    parser.add_argument(
        "--username",
        required=True,
        help="Git username"
    )

    parser.add_argument(
        "--email",
        required=True,
        help="Git email"
    )

    parser.add_argument(
        "--token",
        required=True,
        help="GitHub Personal Access Token"
    )

    parser.add_argument(
        "--repository",
        required=True,
        help="GitHub repository (owner/repo)"
    )

    args = parser.parse_args()

    print()
    print("========== Git Commit ==========")
    print()

    try:

        configure_git(
            args.username,
            args.email
        )

        stage_changes(
            args.images
        )

        if not has_changes():
            print()
            print("No metadata changes detected.")
            print("Skipping commit.")
            print()

            sys.exit(0)

        commit_changes(
            args.version
        )

        push_changes(
            args.token,
            args.repository
        )

        print()
        print("Git metadata committed successfully.")
        print()
        print("================================")

    except Exception as e:

        print()
        print("ERROR:", e)
        print()

        sys.exit(1)


if __name__ == "__main__":
    main()
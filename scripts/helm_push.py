#!/usr/bin/env python3

"""
Helm Chart Upload Utility

Responsibilities
----------------
1. Verify packaged Helm chart exists
2. Upload chart to Artifactory
3. Validate upload

Example
-------

python scripts/helm_push.py \
    --chart dist/devops-asset-inventory-1.2.0.tgz \
    --repo-url https://artifacts.versa-networks.com/repository/versa-helm/ruthwik/ \
    --username versaci \
    --password ****
"""

import argparse
import os
import subprocess
import sys


def run(cmd):

    print(f"\n>>> {' '.join(cmd[:-2])} ********")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(result.stderr)
        sys.exit(result.returncode)

    print(result.stdout)

    return result


def main():

    parser = argparse.ArgumentParser(
        description="Upload Helm Chart"
    )

    parser.add_argument(
        "--chart",
        required=True,
        help="Packaged Helm Chart (.tgz)"
    )

    parser.add_argument(
        "--repo-url",
        required=True,
        help="Artifactory Helm Repository"
    )

    parser.add_argument(
        "--username",
        required=True
    )

    parser.add_argument(
        "--password",
        required=True
    )

    args = parser.parse_args()

    if not os.path.isfile(args.chart):
        print(f"\nERROR : Chart not found : {args.chart}")
        sys.exit(1)

    print("=" * 60)
    print("Uploading Helm Chart")
    print("=" * 60)

    command = [
        "curl",
        "--fail",
        "--silent",
        "--show-error",
        "--upload-file",
        args.chart,
        "-u",
        f"{args.username}:{args.password}",
        args.repo_url
    ]

    run(command)

    print("\n")
    print("=" * 60)
    print("Helm Chart Uploaded Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()
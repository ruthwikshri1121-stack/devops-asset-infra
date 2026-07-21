#!/usr/bin/env python3

"""
Helm Chart Packaging Utility

Responsibilities
----------------
1. Validate Helm chart
2. Update chart dependencies
3. Package Helm chart
4. Store packaged chart in output directory

Example
-------

python scripts/helm_package.py \
    --chart-dir helm/devops-asset-inventory \
    --chart-version 1.2.0 \
    --app-version 1.6.2 \
    --output-dir dist
"""

import argparse
import os
import subprocess
import sys


# ----------------------------------------------------------
# Helper
# ----------------------------------------------------------

def run(cmd):
    print(f"\n>>> {' '.join(cmd)}")

    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("\nERROR: Command failed.")
        sys.exit(result.returncode)


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Package Helm Chart"
    )

    parser.add_argument(
        "--chart-dir",
        required=True,
        help="Path to Helm chart"
    )

    parser.add_argument(
        "--chart-version",
        required=True,
        help="Chart Version"
    )

    parser.add_argument(
        "--app-version",
        required=True,
        help="Docker Image Version"
    )

    parser.add_argument(
        "--output-dir",
        default="dist",
        help="Package Output Directory"
    )

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print("=" * 60)
    print("Packaging Helm Chart")
    print("=" * 60)

    #
    # Step 1
    #

    print("\n[1/3] Linting Chart")

    run([
        "helm",
        "lint",
        args.chart_dir
    ])

    #
    # Step 2
    #

    print("\n[2/3] Updating Dependencies")

    run([
        "helm",
        "dependency",
        "update",
        args.chart_dir
    ])

    #
    # Step 3
    #

    print("\n[3/3] Packaging Chart")

    run([
        "helm",
        "package",
        args.chart_dir,
        "--version",
        args.chart_version,
        "--app-version",
        args.app_version,
        "--destination",
        args.output_dir
    ])

    package = os.path.join(
        args.output_dir,
        f"devops-asset-inventory-{args.chart_version}.tgz"
    )

    print("\n")
    print("=" * 60)
    print("Helm Package Created Successfully")
    print("=" * 60)
    print(package)
    print("=" * 60)


if __name__ == "__main__":
    main()
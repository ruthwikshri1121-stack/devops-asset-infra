#!/usr/bin/env python3

"""
Helm Deployment Utility

Responsibilities
----------------
1. Update Helm repositories
2. Deploy Helm chart
3. Wait for rollout
4. Verify deployment

Example
-------

python scripts/helm_deploy.py \
    --release asset-demo \
    --namespace ruthwik \
    --repo versa-helm \
    --chart devops-asset-inventory \
    --chart-version 1.2.0 \
    --image-tag 1.6.2
"""

import argparse
import subprocess
import sys


def run(cmd):

    print(f"\n>>> {' '.join(cmd)}")

    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("\nERROR : Command Failed")
        sys.exit(result.returncode)


def main():

    parser = argparse.ArgumentParser(
        description="Deploy Helm Chart"
    )

    parser.add_argument(
        "--release",
        required=True
    )

    parser.add_argument(
        "--namespace",
        required=True
    )

    parser.add_argument(
        "--repo",
        required=True
    )

    parser.add_argument(
        "--chart",
        required=True
    )

    parser.add_argument(
        "--chart-version",
        required=True
    )

    parser.add_argument(
        "--image-tag",
        required=True
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Deploying Helm Chart")
    print("=" * 60)

    #
    # Update Repository
    #

    print("\n[1/5] Updating Helm Repository")

    run([
        "helm",
        "repo",
        "update"
    ])

    #
    # Upgrade / Install
    #

    print("\n[2/5] Deploying Chart")

    run([
        "helm",
        "upgrade",
        "--install",
        args.release,
        f"{args.repo}/{args.chart}",
        "--namespace",
        args.namespace,
        "--version",
        args.chart_version,
        "--set",
        f"image.tag={args.image_tag}",
        "--wait",
        "--timeout",
        "5m"
    ])

    #
    # Rollout
    #

    print("\n[3/5] Waiting For Rollout")

    run([
        "kubectl",
        "rollout",
        "status",
        f"deployment/{args.release}",
        "-n",
        args.namespace,
        "--timeout=300s"
    ])

    #
    # Pods
    #

    print("\n[4/5] Pods")

    run([
        "kubectl",
        "get",
        "pods",
        "-n",
        args.namespace
    ])

    #
    # Services
    #

    print("\n[5/5] Services")

    run([
        "kubectl",
        "get",
        "svc",
        "-n",
        args.namespace
    ])

    print("\n")
    print("=" * 60)
    print("Deployment Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()
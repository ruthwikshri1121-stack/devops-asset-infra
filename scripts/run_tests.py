import argparse
import subprocess
import sys

from config import get_app_repo


def run_tests(app_repo=None):
    """
    Run application unit tests.
    """

    app_repo = get_app_repo(app_repo)

    tests_dir = app_repo / "tests"

    if not tests_dir.exists():
        raise FileNotFoundError(
            f"Tests directory not found: {tests_dir}"
        )

    command = [
        "python3",
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests",
        "-p",
        "test_*.py",
        "-v",
    ]

    print("\n========== Running Unit Tests ==========")
    print(f"Application : {app_repo}")
    print(f"Tests Folder: {tests_dir}")
    print()

    print("Executing:")
    print(" ".join(command))
    print()

    try:
        subprocess.run(
            command,
            cwd=app_repo,
            check=True,
        )

        print("\n========================================")
        print("All unit tests passed successfully!")
        print("========================================\n")

    except subprocess.CalledProcessError as exc:
        print("\n========================================")
        print("Unit tests FAILED!")
        print("========================================\n")
        sys.exit(exc.returncode)


def main():

    parser = argparse.ArgumentParser(
        description="Run application unit tests"
    )

    parser.add_argument(
        "--app-repo",
        default=None,
        help="Path to the application repository",
    )

    args = parser.parse_args()

    run_tests(args.app_repo)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# coding: utf-8
import sys
from pathlib import Path
from requests import get
from yaml import safe_load


PWD = Path(__file__).parent.resolve()
CONFORMANCE_TEST_FILES = {
    "v1.0": PWD.joinpath("conformance_test_v1.0.yaml"),
    "v1.1": PWD.joinpath("conformance_test_v1.1.yaml"),
    "v1.2": PWD.joinpath("conformance_test_v1.2.yaml"),
}
FILE_URL_BASE = {
    "v1.0": "https://raw.githubusercontent.com/common-workflow-language/common-workflow-language/main/v1.0/",  # noqa: E501
    "v1.1": "",  # noqa: E501
    "v1.2": "",  # noqa: E501
}


def usage():
    """usage function"""
    print("Usage: python3 download_test.py <v1.0 | v1.1 | v1.2>")
    sys.exit(1)


def download_file(url):
    """Downloads a file from a URL and returns the content."""
    response = get(url)
    if response.status_code != 200:
        raise Exception("Failed to download file: {}".format(url))
    return response.text


def main():
    """main function"""
    if len(sys.argv) != 2 or sys.argv[1] not in ["v1.0", "v1.1", "v1.2"]:
        usage()
    with CONFORMANCE_TEST_FILES[sys.argv[1]].open("r") as f:
        tests = safe_load(f)
    for test in tests:
        print("Downloading {}".format(test["id"]))
        try:
            tool_path = PWD.joinpath(test["tool"])
            tool_path.parent.mkdir(parents=True, exist_ok=True)
            tool = download_file(FILE_URL_BASE[sys.argv[1]] + test["tool"])
            with tool_path.open("w") as f:
                f.write(tool)
        except Exception as e:
            print("Failed to download {}' tool: {}".format(test["id"], e))
        try:
            job_path = PWD.joinpath(test["job"])
            job_path.parent.mkdir(parents=True, exist_ok=True)
            job = download_file(FILE_URL_BASE[sys.argv[1]] + test["job"])
            with job_path.open("w") as f:
                f.write(job)
        except Exception as e:
            print("Failed to download {}'s job: {}".format(test["id"], e))


if __name__ == "__main__":
    main()

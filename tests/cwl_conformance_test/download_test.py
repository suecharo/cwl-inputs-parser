#!/usr/bin/env python3
# coding: utf-8
import sys
from pathlib import Path

from neko_punch.utils import download_file
from yaml import safe_load

PWD = Path(__file__).parent.resolve()
CONFORMANCE_TEST_FILES = {
    "v1.0": PWD.joinpath("conformance_test_v1.0.yaml"),
    "v1.1": PWD.joinpath("conformance_test_v1.1.yaml"),
    "v1.2": PWD.joinpath("conformance_test_v1.2.yaml"),
}
FILE_URL_BASE = {
    "v1.0": "https://raw.githubusercontent.com/common-workflow-language/common-workflow-language/main/v1.0/",  # noqa: E501
    "v1.1": "https://raw.githubusercontent.com/common-workflow-language/cwl-v1.1/main/",  # noqa: E501
    "v1.2": "https://raw.githubusercontent.com/common-workflow-language/cwl-v1.2/main/",  # noqa: E501
}


def usage():
    """usage function"""
    print("Usage: python3 download_test.py <v1.0 | v1.1 | v1.2>")


def main():
    """main function"""
    if len(sys.argv) != 2 or sys.argv[1] not in ["v1.0", "v1.1", "v1.2"]:
        usage()
        sys.exit(1)
    with CONFORMANCE_TEST_FILES[sys.argv[1]].open("r") as f:
        tests = safe_load(f)
    dest_dir = PWD.joinpath(sys.argv[1])
    dest_dir.mkdir(exist_ok=True)
    for test in tests:
        try:
            print("Downloading {}".format(test["id"]))
        except KeyError:
            print("Downloading {}".format(test["label"]))
        try:
            tool_path = dest_dir.joinpath(Path(test["tool"]).name)
            tool = download_file(FILE_URL_BASE[sys.argv[1]] + test["tool"])
            with tool_path.open("w") as f:
                f.write(tool)
        except Exception as e:
            print("Failed to download {}'s tool: {}".format(test["id"], e))
            print(test["doc"])
        try:
            job_path = dest_dir.joinpath(Path(test["job"]).name)
            job = download_file(FILE_URL_BASE[sys.argv[1]] + test["job"])
            with job_path.open("w") as f:
                f.write(job)
        except Exception as e:
            print("Failed to download {}'s job: {}".format(test["id"], e))
            print(test["doc"])


if __name__ == "__main__":
    main()

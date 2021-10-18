#!/usr/bin/env python3
# coding: utf-8
import sys
from pathlib import Path

from yaml import safe_load

CONFORMANCE_TEST_PATH = Path(__file__).parent.joinpath("conformance_test_v1.2_fixed.yaml")  # noqa: E501


def main():
    if len(sys.argv) < 2:
        print("Usage: show_test_by_id.py <test_ids>")
        sys.exit(1)
    with CONFORMANCE_TEST_PATH.open(mode="r", encoding="utf-8") as f:
        conformance_test = safe_load(f)
    ids = list(map(str, sys.argv[1:]))
    for test in conformance_test:
        if str(test["id"]) in ids:
            print(test["tool"])
            wf_path = Path(__file__).parent.joinpath(test["tool"])  # noqa: E501
            with wf_path.open(mode="r", encoding="utf-8") as f:
                print(f.read())


if __name__ == "__main__":
    main()

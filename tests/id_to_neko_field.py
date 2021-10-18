#!/usr/bin/env python3
# coding: utf-8
import sys
from pathlib import Path
from pprint import pprint

from neko_punch.utils import wf_path_to_neko_fields
from yaml import safe_load

CONFORMANCE_TEST_PATH = Path(__file__).parent.joinpath("cwl_conformance_test/conformance_test_v1.2_fixed.yaml")  # noqa: E501


def main():
    if len(sys.argv) != 2:
        print("Usage: id_to_neko_filed.py <test_id>")
        sys.exit(1)
    with CONFORMANCE_TEST_PATH.open(mode="r", encoding="utf-8") as f:
        conformance_test = safe_load(f)
    for test in conformance_test:
        if str(test["id"]) == str(sys.argv[1]):
            wf_path = Path(__file__).parent.joinpath("cwl_conformance_test").joinpath(test["tool"])  # noqa: E501
            neko_fields = wf_path_to_neko_fields(wf_path)
            pprint(neko_fields)


if __name__ == "__main__":
    main()

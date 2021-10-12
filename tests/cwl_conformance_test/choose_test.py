#!/usr/bin/env python3
# coding: utf-8
from pprint import pprint
from neko_punch.utils import fetch_document
from cwl_utils.parser import load_document
import sys
from pathlib import Path
from yaml import safe_load, dump


PWD = Path(__file__).parent.resolve()


def usage():
    """usage function"""
    print("Usage: python3 choose_test.py <v1.0 | v1.1 | v1.2>")  # noqa: E501


def has_streamable(cwl_obj):
    """check if the cwl object has a streamable input field"""
    print("=" * 40)
    pprint(cwl_obj)
    print("-" * 40)
    if "inputs" in cwl_obj:
        for field in cwl_obj["inputs"]:
            pprint(field)
    return False


def main():
    """main function"""
    if len(sys.argv) != 2 or sys.argv[1] not in ["v1.0", "v1.1", "v1.2"]:
        usage()
        sys.exit(1)
    conformance_test_path = \
        PWD.joinpath(f"conformance_test_{sys.argv[1]}.yaml")
    with conformance_test_path.open("r") as f:
        tests = safe_load(f)
    chosen_tests = []
    for test in tests:
        if 'tool' not in test:
            continue
        tool = f"{sys.argv[1]}/{test['tool'].split('/')[-1]}" if "tool" in test else ""  # noqa: E501
        job = f"{sys.argv[1]}/{test['job'].split('/')[-1]}" if "job" in test else ""  # noqa: E501
        cwl_obj = load_document(fetch_document(PWD.joinpath(tool)))
        has_streamable(cwl_obj)
        chosen_test = {
            "id": test.get("id", ""),
            "label": test.get("label", "").replace("\n", " ").strip(),
            "doc": test.get("doc", "").replace("\n", " ").strip(),
            "tool": tool.strip(),
            "job": job.strip(),
            "disable": False,
            "reason": ""
        }
        chosen_tests.append(chosen_test)
    # chosen_tests_path = PWD.joinpath(f"conformance_test_{sys.argv[1]}_chosen.yaml")  # noqa: E501
    # with chosen_tests_path.open("w") as f:
    #     f.write(dump(chosen_tests, default_flow_style=False))


if __name__ == "__main__":
    main()

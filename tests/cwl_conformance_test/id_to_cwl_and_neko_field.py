#!/usr/bin/env python3
# coding: utf-8
import sys
from pathlib import Path
from pprint import pprint

from cwl_utils.parser import load_document
from neko_punch.utils import (as_uri, extract_main_tool, fetch_document,
                              wf_path_to_neko_fields)
from yaml import safe_load

CONFORMANCE_TEST_PATH = Path(__file__).parent.joinpath("conformance_test_v1.2_fixed.yaml")  # noqa: E501


def main():
    if len(sys.argv) < 2:
        print("Usage: id_to_cwl_and_neko_field.py <test_ids>")
        sys.exit(1)
    with CONFORMANCE_TEST_PATH.open(mode="r", encoding="utf-8") as f:
        conformance_test = safe_load(f)
    ids = [s.strip("[],") for s in map(str, sys.argv[1:])]
    for test in conformance_test:
        if str(test["id"]) in ids:
            print(f"--- {test['id']}: {test['tool']} ---")
            wf_path = Path(__file__).parent.joinpath(test["tool"])  # noqa: E501
            cwl_obj = extract_main_tool(load_document(fetch_document(wf_path), baseuri=as_uri(wf_path)))  # noqa: E501
            for inp in cwl_obj.inputs:
                pprint(inp.__dict__)
                if isinstance(inp.type, str):
                    pass
                elif isinstance(inp.type, list):
                    for t in inp.type:
                        if not isinstance(t, str):
                            pprint(t.__dict__)
                else:
                    pprint(inp.type.__dict__)
            try:
                neko_fields = wf_path_to_neko_fields(wf_path)
                pprint(neko_fields)
            except Exception:
                print("Failed to convert to neko_punch fields")


if __name__ == "__main__":
    main()

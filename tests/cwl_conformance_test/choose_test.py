#!/usr/bin/env python3
# coding: utf-8
import sys
from pathlib import Path
from pprint import pprint

from cwl_utils.parser import load_document
from neko_punch.utils import fetch_document
from yaml import safe_dump, safe_load

PWD = Path(__file__).parent.resolve()


def usage():
    """usage function"""
    print("Usage: python3 choose_test.py <v1.0 | v1.1 | v1.2>")  # noqa: E501


def check_special_field(cwl_obj):
    for field in cwl_obj.inputs:
        if field.secondaryFiles:
            pprint("secondaryFiles")
            pprint(field.secondaryFiles)
        if field.streamable:
            # Only valid when type: File or is an array of items: File.
            # A value of true indicates that the file is read or written sequentially without seeking. An implementation may use this flag to indicate whether it is valid to stream file contents using a named pipe. Default: false. # noqa: E501
            pprint("streamable")
            pprint(field.streamable)
        if field.format:
            # Only valid when type: File or is an array of items: File.
            # This must be one or more IRIs of concept nodes that represents file formats which are allowed as input to this parameter, preferrably defined within an ontology. If no ontology is available, file formats may be tested by exact match. # noqa: E501
            pprint("format")
            pprint(field.format)
        if field.loadContents:
            # Only valid when type: File or is an array of items: File.
            # Read up to the first 64 KiB of text from the file and place it in the "contents" field of the file object for use by expressions. # noqa: E501
            pprint("loadContents")
            pprint(field.loadContents)
        if field.loadListing:
            # Only valid when type: Directory or is an array of items: Directory. # noqa: E501
            # Specify the desired behavior for loading the listing field of a Directory object for use by expressions. # noqa: E501
            # The order of precedence for loadListing is :
            # loadListing on an individual parameter
            # Inherited from LoadListingRequirement
            # By default: no_listing
            pprint("loadListing")
            pprint(field.loadListing)
        if len(field.extension_fields) != 0:
            pprint("extension_fields")
            pprint(field.extension_fields)


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
        if "id" not in test and "label" not in test:
            continue

        chosen_test = {
            "id": test.get("id", ""),
            "label": test.get("label", "").replace("\n", " ").strip(),
            "doc": test.get("doc", "").replace("\n", " ").strip(),
            "tool": None,
            "job": None,
            "disable": False,
            "reason": None,
        }
        if 'tool' not in test:
            chosen_test['disable'] = True
            chosen_test['reason'] = "No tool"
        tool = f"{sys.argv[1]}/{test['tool'].split('/')[-1]}".strip() if "tool" in test else ""  # noqa: E501
        job = f"{sys.argv[1]}/{test['job'].split('/')[-1]}".strip() if "job" in test else ""  # noqa: E501
        if "#" in tool:
            tool = tool.split("#")[0]
        if "#" in job:
            job = job.split("#")[0]
        chosen_test["tool"] = tool
        chosen_test["job"] = job

        try:
            cwl_obj = load_document(fetch_document(PWD.joinpath(tool)))
        except Exception:
            chosen_test["disable"] = True
            chosen_test["reason"] = "Failed to load tool"
        if isinstance(cwl_obj, list):
            for obj in cwl_obj:
                if obj.class_ == "Workflow" or obj.id.split("#")[-1] == "main":
                    cwl_obj = obj
                    break

        print(chosen_test["tool"])
        check_special_field(cwl_obj)

        chosen_tests.append(chosen_test)
    chosen_tests_path = PWD.joinpath(f"conformance_test_{sys.argv[1]}_chosen.yaml")  # noqa: E501
    with chosen_tests_path.open("w") as f:
        f.write(safe_dump(chosen_tests, default_flow_style=False))


if __name__ == "__main__":
    main()

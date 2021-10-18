#!/usr/bin/env python3
# coding: utf-8
import sys
from pathlib import Path
from pprint import pprint

from cwl_utils.parser import load_document
from cwl_utils.parser.cwl_v1_2 import (CommandInputArraySchema,
                                       CommandInputEnumSchema,
                                       CommandInputRecordSchema,
                                       InputArraySchema, InputRecordSchema)
from neko_punch.utils import extract_main_tool, fetch_document
from yaml import safe_load


def main():
    if len(sys.argv) != 2:
        print("Usage: extract_all_inputs.py <v1.0 | v1.1 | v1.2>")
        sys.exit(1)
    test_file_path = Path(__file__).parent.joinpath(f"conformance_test_{sys.argv[1]}_chosen.yaml")  # noqa: E501
    with open(test_file_path, mode="r", encoding="utf-8") as f:
        tests = safe_load(f)
    # type_set = set()
    for test in tests:
        if test["disable"]:
            continue
        tool_path = Path(__file__).parent.joinpath(test["tool"])
        cwl_obj = extract_main_tool(load_document(fetch_document(tool_path)))
        for inp in cwl_obj.inputs:
            if isinstance(inp.type, str):
                # type_set.add(inp.type)
                if inp.type == "boolean":
                    # pprint(test["tool"])
                    # pprint(inp.__dict__)
                    pass
                elif inp.type == "int":
                    # pprint(test["tool"])
                    # pprint(inp.__dict__)
                    pass
                elif inp.type == "string":
                    # pprint(test["tool"])
                    # pprint(inp.__dict__)
                    pass
                elif inp.type == "File":
                    # pprint(test["tool"])
                    # pprint(inp.__dict__)
                    pass
                elif inp.type == "stdin":
                    # pprint(test["tool"])
                    # pprint(inp.__dict__)
                    pass
                elif inp.type == "Directory":
                    # pprint(test["tool"])
                    # pprint(inp.__dict__)
                    pass
                elif inp.type == "Any":
                    # pprint(test["tool"])
                    # pprint(inp.__dict__)
                    pass
                else:
                    # pprint(test["tool"])
                    # pprint(inp.__dict__)
                    pass
            elif isinstance(inp.type, list):
                # pprint(test["tool"])
                # pprint(inp.__dict__)
                pass
            elif isinstance(inp.type, CommandInputArraySchema):
                # pprint(test["tool"])
                # pprint(inp.__dict__)
                pass
            elif isinstance(inp.type, CommandInputEnumSchema):
                # [TODO] not support
                # pprint(test["tool"])
                # pprint(inp.__dict__)
                pass
            elif isinstance(inp.type, CommandInputRecordSchema):
                # [TODO] not support
                # pprint(test["tool"])
                # pprint(inp.__dict__)
                pass
            elif isinstance(inp.type, InputArraySchema):
                if isinstance(inp.type.items, InputRecordSchema):
                    # [TODO] not support
                    # pprint(test["tool"])
                    # pprint(inp.type.__dict__)
                    pass
                else:
                    # pprint(test["tool"])
                    # pprint(inp.__dict__)
                    # pprint(inp.type.__dict__)
                    pass
            elif isinstance(inp.type, InputRecordSchema):
                pprint(test["tool"])
                pprint(inp.__dict__)
                pass
            else:
                # pprint(test["tool"])
                # pprint(inp.__dict__)
                pass
    # print(type_set)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# coding: utf-8
from pathlib import Path
from pprint import pprint

from cwl_utils.parser import load_document
from cwl_utils.parser.cwl_v1_2 import (CommandInputArraySchema,
                                       CommandInputEnumSchema,
                                       CommandInputRecordSchema,
                                       InputArraySchema, InputRecordSchema)
from neko_punch.utils import Neko, extract_main_tool, fetch_document
from yaml import safe_load


def main():
    conformance_test_path = Path(__file__).parent.joinpath("conformance_test_v1.2_fixed.yaml")  # noqa: E501
    with conformance_test_path.open(mode="r", encoding="utf-8") as f:
        tests = safe_load(f)
    a = set()
    for test in tests:
        tool_path = Path(__file__).parent.joinpath(test["tool"])
        try:
            cwl_obj = extract_main_tool(load_document(fetch_document(tool_path)))  # noqa: E501
        except Exception:
            continue
        try:
            neko = Neko(cwl_obj)
            neko.punch()
        except Exception:
            continue

        for inp in cwl_obj.inputs:
            if isinstance(inp.type, str):
                # pprint(f"--- {test['id']}: {test['tool']} ---")
                # pprint(inp.__dict__)
                pass
            elif isinstance(inp.type, list):
                if len(inp.type) == 1:
                    if isinstance(inp.type[0], str):
                        # pprint(f"--- {test['id']}: {test['tool']} ---")
                        # pprint(inp.__dict__)
                        pass
                    elif isinstance(inp.type[0], CommandInputArraySchema):
                        # pprint(f"--- {test['id']}: {test['tool']} ---")
                        # pprint(inp.__dict__)
                        pass
                    elif isinstance(inp.type[0], InputArraySchema):
                        # pprint(f"--- {test['id']}: {test['tool']} ---")
                        # pprint(inp.__dict__)
                        pass
                    else:
                        # pprint(f"--- {test['id']}: {test['tool']} ---")
                        # pprint(inp.__dict__)
                        pass
                elif len(inp.type) == 2:
                    if 'null' in inp.type:
                        # pprint(f"--- {test['id']}: {test['tool']} ---")
                        # pprint(inp.__dict__)
                        pass
                    else:
                        # pprint(f"--- {test['id']}: {test['tool']} ---")
                        # pprint(inp.__dict__)
                        pass
                else:
                    # pprint(f"--- {test['id']}: {test['tool']} ---")
                    # pprint(inp.__dict__)
                    pass
            elif isinstance(inp.type, CommandInputArraySchema):
                a.add(test['id'])
                # pprint(f"--- {test['id']}: {test['tool']} ---")
                # pprint(inp.__dict__)
                pass
            elif isinstance(inp.type, CommandInputEnumSchema):
                a.add(test['id'])
                # pprint(f"--- {test['id']}: {test['tool']} ---")
                # pprint(inp.__dict__)
                pass
            elif isinstance(inp.type, CommandInputRecordSchema):
                a.add(test['id'])
                # pprint(f"--- {test['id']}: {test['tool']} ---")
                # pprint(inp.__dict__)
                pass
            elif isinstance(inp.type, InputArraySchema):
                a.add(test['id'])
                if isinstance(inp.type.items, InputRecordSchema):
                    # pprint(f"--- {test['id']}: {test['tool']} ---")
                    # pprint(inp.__dict__)
                    pass
                else:
                    # pprint(f"--- {test['id']}: {test['tool']} ---")
                    # pprint(inp.__dict__)
                    pass
            elif isinstance(inp.type, InputRecordSchema):
                a.add(test['id'])
                # pprint(f"--- {test['id']}: {test['tool']} ---")
                # pprint(inp.__dict__)
                pass
            else:
                a.add(test['id'])
                # pprint(f"--- {test['id']}: {test['tool']} ---")
                # pprint(inp.__dict__)
                pass
    print(list(a))


if __name__ == "__main__":
    main()

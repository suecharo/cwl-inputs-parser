#!/usr/bin/env python3
# coding: utf-8
import sys
from pathlib import Path

from cwl_utils.parser import load_document
from cwl_utils.parser.cwl_v1_2 import (CommandInputArraySchema,
                                       CommandInputEnumSchema,
                                       CommandInputRecordSchema,
                                       InputArraySchema, InputRecordSchema)
from neko_punch.utils import extract_main_tool, fetch_document
from yaml import safe_load

# from pprint import pprint



def main():
    if len(sys.argv) != 2:
        print("Usage: extract_all_inputs.py <v1.0 | v1.1 | v1.2>")
        sys.exit(1)
    test_file_path = Path(__file__).parent.joinpath(f"conformance_test_{sys.argv[1]}_fixed.yaml")  # noqa: E501
    with open(test_file_path, mode="r", encoding="utf-8") as f:
        tests = safe_load(f)
    # type_set = set()
    for test in tests:
        tool_path = Path(__file__).parent.joinpath(test["tool"])
        try:
            cwl_obj = extract_main_tool(load_document(fetch_document(tool_path)))  # noqa: E501
        except Exception:
            pass
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
                    # [TODO] not support
                    # 'v1.2/import_schema-def_packed.cwl'
                    # 'v1.2/anon_enum_inside_array_inside_schemadef.cwl'
                    # 'v1.2/record-sd-secondaryFiles.cwl'
                    # pprint(test["tool"])
                    # pprint(inp.__dict__)
                    pass
            elif isinstance(inp.type, list):
                if inp.default:
                    # [TODO] not support
                    # 'v1.2/io-union-input-default-wf.cwl'
                    # pprint(test["tool"])
                    # pprint(inp.__dict__)
                    pass
                else:
                    if len(inp.type) == 1:
                        # inp.type = inp.type[0]
                        # 'v1.2/count-lines12-wf.cwl'
                        # 'v1.2/valueFrom-constant.cwl'
                        pass
                    elif len(inp.type) == 2:
                        if 'null' not in inp.type:
                            # [TODO] not support (union type)
                            # pprint(test["tool"])
                            # pprint(inp.__dict__)
                            pass
                        else:
                            # pprint(test["tool"])
                            # pprint(inp.__dict__)
                            pass
                    else:
                        # [TODO] not support (union type)
                        # 'v1.2/io-file-or-files.cwl'
                        pass
            elif isinstance(inp.type, CommandInputArraySchema):
                # pprint(test["tool"])
                # pprint(inp.__dict__)
                pass
            elif isinstance(inp.type, CommandInputEnumSchema):
                # [TODO] not support
                # Not exist in conformance test v1.2
                # pprint(test["tool"])
                # pprint(inp.__dict__)
                pass
            elif isinstance(inp.type, CommandInputRecordSchema):
                # [TODO] not support
                # Failed to `cwltool --make-template`
                # 'v1.2/record-output.cwl'
                # 'v1.2/anon_enum_inside_array.cwl'
                # 'v1.2/record-in-secondaryFiles.cwl'
                # 'v1.2/record-in-format.cwl'
                # 'v1.2/record-out-format.cwl'
                # pprint(test["tool"])
                # pprint(inp.__dict__)
                pass
            elif isinstance(inp.type, InputArraySchema):
                if isinstance(inp.type.items, InputRecordSchema):
                    # [TODO] not support
                    # Failed to `cwltool --make-template`
                    # 'v1.2/scatter-valuefrom-wf1.cwl'
                    # 'v1.2/scatter-valuefrom-wf2.cwl'
                    # 'v1.2/scatter-valuefrom-wf3.cwl'
                    # 'v1.2/scatter-valuefrom-wf4.cwl'
                    # 'v1.2/scatter-valuefrom-wf5.cwl'
                    # 'v1.2/scatter-valuefrom-inputs-wf1.cwl'
                    # pprint(test["tool"])
                    # pprint(inp.__dict__)
                    pass
                else:
                    # pprint(test["tool"])
                    # pprint(inp.__dict__)
                    # pprint(inp.type.__dict__)
                    pass
            elif isinstance(inp.type, InputRecordSchema):
                # [TODO] not support
                # 'v1.2/step-valuefrom-wf.cwl'
                # 'v1.2/record-output-wf.cwl'
                # 'v1.2/record-in-secondaryFiles-wf.cwl'
                # 'v1.2/record-in-secondaryFiles-missing-wf.cwl'
                # pprint(test["tool"])
                # pprint(inp.__dict__)
                pass
            else:
                # pprint(test["tool"])
                # pprint(inp.__dict__)
                pass
    # print(type_set)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# coding: utf-8
from pathlib import Path
from pprint import pprint

from neko_punch.utils import UnsupportedValueError, wf_path_to_neko_fields
from schema_salad.exceptions import ValidationException
from yaml import safe_load

CONFORMANCE_TEST_PATH = Path(__file__).parent.joinpath("conformance_test_v1.2_fixed.yaml")  # noqa: E501


def main():
    with CONFORMANCE_TEST_PATH.open(mode="r", encoding="utf-8") as f:
        conformance_test = safe_load(f)
    for test in conformance_test:
        wf_path = Path(__file__).parent.joinpath(test["tool"])  # noqa: E501
        try:
            neko_fields = wf_path_to_neko_fields(wf_path)
        except Exception as e:
            if isinstance(e, ValidationException):
                # print(test["id"])
                pass
            elif isinstance(e, UnsupportedValueError):
                if "CommandInputRecordSchema" in e.args[0]:
                    # print(test["id"])
                    pass
                elif "InputRecordSchema field does" in e.args[0]:
                    # print(test["id"])
                    pass
                elif "InputRecordSchema field in the InputArraySchema" in e.args[0]:  # noqa: E501
                    # print(test["id"])
                    pass
                elif "union field" in e.args[0]:
                    # print(test["id"])
                    pass
                elif "an unsupported format" in e.args[0]:
                    # print(test["id"])
                    pass
                else:
                    # print(test["id"])
                    # print(e)
                    pass
            else:
                # print(test["id"])
                # print(e)
                pass
            continue
        # print(test["id"])
        # pprint(neko_fields)


if __name__ == "__main__":
    main()
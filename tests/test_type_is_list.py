#!/usr/bin/env python3
# coding: utf-8
from copy import deepcopy
from pathlib import Path

from cwl_inputs_parser.utils import Inputs, wf_location_to_inputs
from cwl_utils.parser.cwl_v1_2 import CommandInputArraySchema, InputArraySchema
from yaml import safe_load

from const import CONFORMANCE_TEST_PATH, CWL_UTILS_OBJ_TEMPLATE

CONFORMANCE_TEST_IDS = [4, 5, 50, 51, 52, 63, 68, 69, 100, 101, 109, 110, 114, 125, 130, 146, 147, 180, 183, 184, 186, 187, 219, 220, 221, 222, 225]  # noqa: E501


def test_using_conformance_test():
    conformance_test = safe_load(CONFORMANCE_TEST_PATH.open(mode="r", encoding="utf-8"))  # noqa: E501
    for test in conformance_test:
        if test["id"] in CONFORMANCE_TEST_IDS:
            wf_path = Path(__file__).parent.joinpath("cwl_conformance_test").joinpath(test["tool"])  # noqa: E501
            wf_location_to_inputs(wf_path)


def test_required_false():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = ["null", "boolean"]
    inputs = Inputs(cwl_obj)
    result = inputs.fields[0]
    assert result.type == "boolean"
    assert result.required is False


def test_input_array_schema():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = [InputArraySchema(items="File", type="array")]
    inputs = Inputs(cwl_obj)
    result = inputs.fields[0]
    assert result.type == "File"
    assert result.array is True


def test_command_input_array_schema():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = [CommandInputArraySchema(items="File", type="array")]  # noqa: E501
    inputs = Inputs(cwl_obj)
    result = inputs.fields[0]
    assert result.type == "File"
    assert result.array is True

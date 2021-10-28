#!/usr/bin/env python3
# coding: utf-8
from copy import deepcopy
from pathlib import Path

import pytest
from cwl_inputs_parser.utils import (Inputs, UnsupportedValueError,
                                     wf_location_to_inputs)
from cwl_utils.parser.cwl_v1_2 import (CommandInputArraySchema,
                                       InputArraySchema, SecondaryFileSchema)
from yaml import safe_load

from const import CONFORMANCE_TEST_PATH, CWL_UTILS_OBJ_TEMPLATE

CONFORMANCE_TEST_IDS = [1, 2, 20, 26, 28, 29, 35, 36, 37, 38, 39, 40, 41, 42, 43, 76, 82, 100, 101, 102, 128, 139, 175, 176, 225, 226, 238, 239, 240]  # noqa: E501


def test_using_conformance_test():
    with CONFORMANCE_TEST_PATH.open(mode="r", encoding="utf-8") as f:
        conformance_test = safe_load(f)
    for test in conformance_test:
        if test["id"] in CONFORMANCE_TEST_IDS:
            wf_path = Path(__file__).parent.joinpath("cwl_conformance_test").joinpath(test["tool"])  # noqa: E501
            wf_location_to_inputs(wf_path)


def test_command_input_array_schema_file():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = CommandInputArraySchema(items="File", type="array")  # noqa: E501
    inputs = Inputs(cwl_obj)
    result = inputs.fields[0]
    assert result.type == "File"
    assert result.array is True


def test_command_input_array_schema_int():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = CommandInputArraySchema(items="int", type="array")
    inputs = Inputs(cwl_obj)
    result = inputs.fields[0]
    assert result.type == "int"
    assert result.array is True


def test_command_input_array_schema_items_is_unknown():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = CommandInputArraySchema(items="unknown", type="array")  # noqa: E501
    with pytest.raises(UnsupportedValueError) as e:
        Inputs(cwl_obj)
    assert "an unsupported format" in str(e.value)


def test_command_input_array_schema_secondaryFiles():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].secondaryFiles = [
        SecondaryFileSchema(pattern="foo", required=True),
        SecondaryFileSchema(pattern="bar", required=False)
    ]
    cwl_obj.inputs[0].type = CommandInputArraySchema(items="File", type="array")  # noqa: E501
    inputs = Inputs(cwl_obj)
    result = inputs.fields[0]
    assert result.type == "File"
    assert result.array is True
    assert result.secondaryFiles[0].pattern == "foo"
    assert result.secondaryFiles[0].required is True
    assert result.secondaryFiles[1].pattern == "bar"
    assert result.secondaryFiles[1].required is False


def test_input_array_schema_file():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = InputArraySchema(items="File", type="array")
    inputs = Inputs(cwl_obj)
    result = inputs.fields[0]
    assert result.type == "File"
    assert result.array is True


def test_input_array_schema_int():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = InputArraySchema(items="int", type="array")
    inputs = Inputs(cwl_obj)
    result = inputs.fields[0]
    assert result.type == "int"
    assert result.array is True


def test_input_array_schema_items_is_unknown():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = InputArraySchema(items="unknown", type="array")  # noqa: E501
    with pytest.raises(UnsupportedValueError) as e:
        Inputs(cwl_obj)
    assert "an unsupported format" in str(e.value)

#!/usr/bin/env python3
# coding: utf-8
from copy import deepcopy
from pathlib import Path

import pytest
from cwl_inputs_parser.utils import (Inputs, UnsupportedValueError,
                                     wf_location_to_inputs)
from cwl_utils.parser.cwl_v1_2 import CommandInputRecordSchema
from yaml import safe_load

from const import CONFORMANCE_TEST_PATH, CWL_UTILS_OBJ_TEMPLATE

CONFORMANCE_TEST_IDS = [73, 197, 200, 205, 206, 207, 208, 209]


def test_using_conformance_test():
    conformance_test = safe_load(CONFORMANCE_TEST_PATH.open(mode="r", encoding="utf-8"))  # noqa: E501
    for test in conformance_test:
        if test["id"] in CONFORMANCE_TEST_IDS:
            wf_path = Path(__file__).parent.joinpath("cwl_conformance_test").joinpath(test["tool"])  # noqa: E501
            with pytest.raises(UnsupportedValueError) as e:
                wf_location_to_inputs(wf_path)
            assert "CommandInputRecordSchema" in str(e.value)


def test_raise_error():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = CommandInputRecordSchema(type="record")
    with pytest.raises(UnsupportedValueError) as e:
        Inputs(cwl_obj)
    assert "CommandInputRecordSchema" in str(e.value)

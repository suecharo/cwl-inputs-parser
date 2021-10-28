#!/usr/bin/env python3
# coding: utf-8
from copy import deepcopy
from pathlib import Path

from cwl_inputs_parser.utils import Inputs, wf_location_to_inputs
from yaml import safe_load

from const import CONFORMANCE_TEST_PATH, CWL_UTILS_OBJ_TEMPLATE

CONFORMANCE_TEST_IDS = [10, 11, 12, 33, 49, 74, 75, 95, 96, 97, 103, 104, 105, 116, 117, 118, 119, 122, 123, 126, 129, 134, 169, 174, 179, 188, 189, 193, 195, 202, 214, 215, 216, 217, 218, 223, 224, 232, 233, 234, 235, 236, 237, 241, 250, 253, 255, 256]  # noqa: E501


def test_using_conformance_test():
    conformance_test = safe_load(CONFORMANCE_TEST_PATH.open(mode="r", encoding="utf-8"))  # noqa: E501
    for test in conformance_test:
        if test["id"] in CONFORMANCE_TEST_IDS:
            wf_path = Path(__file__).parent.joinpath("cwl_conformance_test").joinpath(test["tool"])  # noqa: E501
            inputs = wf_location_to_inputs(wf_path)
            assert len(inputs.fields) == 0


def test_with_empty_input():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs = []
    inputs = Inputs(cwl_obj)
    assert len(inputs.fields) == 0

#!/usr/bin/env python3
# coding: utf-8
from copy import deepcopy
from pathlib import Path
from typing import OrderedDict

from neko_punch.utils import Neko, wf_path_to_neko_fields
from yaml import safe_load

from const import CONFORMANCE_TEST_PATH, CWL_UTILS_OBJ_TEMPLATE

CONFORMANCE_TEST_IDS = [1, 2, 4, 5, 6, 7, 8, 9, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 30, 31, 32, 34, 44, 45, 46, 47, 48, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 71, 72, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 98, 99, 106, 107, 108, 111, 112, 113, 120, 121, 124, 125, 127, 128, 130, 131, 132, 133, 137, 138, 140, 141, 142, 143, 145, 148, 149, 150, 151, 152, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 170, 171, 172, 173, 177, 178, 181, 185, 190, 191, 192, 194, 196, 199, 210, 211, 212, 213, 225, 227, 228, 229, 230, 231, 242, 243, 244, 245, 246, 247, 248, 249, 251, 252, 257, 'count-lines19-wf']  # noqa: E501


def test_using_conformance_test():
    with CONFORMANCE_TEST_PATH.open(mode="r", encoding="utf-8") as f:
        conformance_test = safe_load(f)
    for test in conformance_test:
        if test["id"] in CONFORMANCE_TEST_IDS:
            wf_path = Path(__file__).parent.joinpath("cwl_conformance_test").joinpath(test["tool"])  # noqa: E501
            wf_path_to_neko_fields(wf_path)


def test_file():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = "File"
    neko = Neko(cwl_obj)
    neko.punch()
    result = neko.results[0]
    assert result.type == "File"
    assert result.required is True


def test_file_default_by_path():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = "File"
    cwl_obj.inputs[0].default = OrderedDict([("class", "File"), ("path", "test.txt")])  # noqa: E501
    neko = Neko(cwl_obj)
    neko.punch()
    result = neko.results[0]
    assert result.type == "File"
    assert result.default == "test.txt"


def test_file_default_by_location():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = "File"
    cwl_obj.inputs[0].default = OrderedDict([("class", "File"), ("location", "test.txt")])  # noqa: E501
    neko = Neko(cwl_obj)
    neko.punch()
    result = neko.results[0]
    assert result.type == "File"
    assert result.default == "test.txt"


def test_any():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = "Any"
    neko = Neko(cwl_obj)
    neko.punch()
    result = neko.results[0]
    assert result.type == "Any"
    assert result.required is True


def test_direcotroy():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = "Directory"
    neko = Neko(cwl_obj)
    neko.punch()
    result = neko.results[0]
    assert result.type == "Directory"
    assert result.required is True


def test_int():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = ["int"]
    neko = Neko(cwl_obj)
    neko.punch()
    result = neko.results[0]
    assert result.type == "int"
    assert result.required is True


def test_string():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = ["string"]
    neko = Neko(cwl_obj)
    neko.punch()
    result = neko.results[0]
    assert result.type == "string"
    assert result.required is True


def test_boolean():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = ["boolean"]
    neko = Neko(cwl_obj)
    neko.punch()
    result = neko.results[0]
    assert result.type == "boolean"
    assert result.required is True

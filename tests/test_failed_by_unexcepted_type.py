#!/usr/bin/env python3
# coding: utf-8
from copy import deepcopy
from pathlib import Path

import pytest
from neko_punch.utils import (Neko, UnsupportedValueError,
                              wf_path_to_neko_fields)
from yaml import safe_load

from const import CONFORMANCE_TEST_PATH, CWL_UTILS_OBJ_TEMPLATE

CONFORMANCE_TEST_IDS = [3, 94, 136, 198, 201]


def test_using_conformance_test():
    with CONFORMANCE_TEST_PATH.open(mode="r", encoding="utf-8") as f:
        conformance_test = safe_load(f)
    for test in conformance_test:
        if test["id"] in CONFORMANCE_TEST_IDS:
            wf_path = Path(__file__).parent.joinpath("cwl_conformance_test").joinpath(test["tool"])  # noqa: E501
            with pytest.raises(UnsupportedValueError) as e:
                wf_path_to_neko_fields(wf_path)
            assert "an unsupported format" in str(e.value)


def test_raise_error():
    cwl_obj = deepcopy(CWL_UTILS_OBJ_TEMPLATE)
    cwl_obj.inputs[0].type = "foobar"
    with pytest.raises(UnsupportedValueError) as e:
        neko = Neko(cwl_obj)
        neko.punch()
    assert "an unsupported format" in str(e.value)

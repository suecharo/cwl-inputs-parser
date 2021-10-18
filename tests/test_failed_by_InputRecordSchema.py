#!/usr/bin/env python3
# coding: utf-8
from pathlib import Path

import pytest
from neko_punch.utils import wf_path_to_neko_fields, UnsupportedValueError
from yaml import safe_load

CONFORMANCE_TEST_PATH = Path(__file__).parent.joinpath("cwl_conformance_test/conformance_test_v1.2_fixed.yaml")  # noqa: E501
FAILED_TESTS = [70, 73, 144, 197, 200, 203, 204, 205, 206, 207, 208, 209]


def test_failed_by_InputRecordSchema():
    with CONFORMANCE_TEST_PATH.open(mode="r", encoding="utf-8") as f:
        conformance_test = safe_load(f)
    for test in conformance_test:
        if test["id"] in FAILED_TESTS:
            wf_path = Path(__file__).parent.joinpath("cwl_conformance_test").joinpath(test["tool"])  # noqa: E501
            with pytest.raises(UnsupportedValueError) as e:
                wf_path_to_neko_fields(wf_path)
            assert "InputRecordSchema field does" in str(e.value)

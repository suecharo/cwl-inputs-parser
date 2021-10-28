#!/usr/bin/env python3
# coding: utf-8
from pathlib import Path

import pytest
from cwl_inputs_parser.utils import (UnsupportedValueError,
                                     wf_location_to_inputs)
from yaml import safe_load

from const import CONFORMANCE_TEST_PATH

CONFORMANCE_TEST_IDS = [115, 153, 154, 155, 156, 167, 168, 182]


def test_using_conformance_test():
    conformance_test = safe_load(CONFORMANCE_TEST_PATH.open(mode="r", encoding="utf-8"))  # noqa: E501
    for test in conformance_test:
        if test["id"] in CONFORMANCE_TEST_IDS:
            wf_path = Path(__file__).parent.joinpath("cwl_conformance_test").joinpath(test["tool"])  # noqa: E501
            with pytest.raises(UnsupportedValueError) as e:
                wf_location_to_inputs(wf_path)
            assert "union field" in str(e.value)

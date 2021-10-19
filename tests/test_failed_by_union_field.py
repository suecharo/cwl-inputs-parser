#!/usr/bin/env python3
# coding: utf-8
from pathlib import Path

import pytest
from neko_punch.utils import UnsupportedValueError, wf_path_to_neko_fields
from yaml import safe_load

from const import CONFORMANCE_TEST_PATH

CONFORMANCE_TEST_IDS = [115, 153, 154, 155, 156, 167, 168, 182]


def test_using_conformance_test():
    with CONFORMANCE_TEST_PATH.open(mode="r", encoding="utf-8") as f:
        conformance_test = safe_load(f)
    for test in conformance_test:
        if test["id"] in CONFORMANCE_TEST_IDS:
            wf_path = Path(__file__).parent.joinpath("cwl_conformance_test").joinpath(test["tool"])  # noqa: E501
            with pytest.raises(UnsupportedValueError) as e:
                wf_path_to_neko_fields(wf_path)
            assert "union field" in str(e.value)

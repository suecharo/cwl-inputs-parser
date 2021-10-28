#!/usr/bin/env python3
# coding: utf-8
from pathlib import Path

from cwl_inputs_parser.utils import Workflow
from cwl_utils.parser.cwl_v1_2 import WorkflowInputParameter

CONFORMANCE_TEST_PATH = Path(__file__).parent.joinpath("cwl_conformance_test/conformance_test_v1.2_fixed.yaml")  # noqa: E501
CWL_UTILS_OBJ_TEMPLATE = Workflow(
    inputs=[
        WorkflowInputParameter(
            default=None,
            doc="test template doc",
            id="test template id",
            label="test template label",
            type=None,
            secondaryFiles=None,
        )
    ],
    outputs=None,
    steps=None,
)

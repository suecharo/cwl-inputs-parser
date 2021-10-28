#!/usr/bin/env python3
# coding: utf-8
import json
from pathlib import Path

import jsonschema
from cwl_inputs_parser.utils import wf_location_to_inputs

ALL_INPUT_CWL_PATH = Path(__file__).parent.joinpath("all_input.cwl")
ALL_INPUT_JSON_PATH = Path(__file__).parent.joinpath("all_input.json")
JSON_SCHEMA = Path(__file__).parent.parent.joinpath("cwl-inputs-parser-schema.json")  # noqa: E501


def test_by_file():
    json_str = wf_location_to_inputs(ALL_INPUT_CWL_PATH).as_json()
    expect = ALL_INPUT_JSON_PATH.read_text(encoding="utf-8").strip()
    assert json_str == expect


def test_by_jsonschema():
    json_str = wf_location_to_inputs(ALL_INPUT_CWL_PATH).as_json()
    schema = json.loads(JSON_SCHEMA.read_text(encoding="utf-8"))
    data = json.loads(json_str)
    jsonschema.validate(data, schema)

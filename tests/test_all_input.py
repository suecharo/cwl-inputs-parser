#!/usr/bin/env python3
# coding: utf-8
import json
from pathlib import Path

import jsonschema
from neko_punch.utils import dump_json, wf_path_to_neko_fields

ALL_INPUT_CWL_PATH = Path(__file__).parent.joinpath("all_input.cwl")
ALL_INPUT_JSON_PATH = Path(__file__).parent.joinpath("all_input.json")
JSON_SCHEMA = Path(__file__).parent.parent.joinpath("neko-fields-schema.json")


def test_by_file():
    json_str = dump_json(wf_path_to_neko_fields(ALL_INPUT_CWL_PATH))
    with ALL_INPUT_JSON_PATH.open(mode="r", encoding="utf-8") as f:
        expect = f.read().strip()
    assert json_str == expect


def test_by_jsonschema():
    json_str = dump_json(wf_path_to_neko_fields(ALL_INPUT_CWL_PATH))
    with JSON_SCHEMA.open(mode="r", encoding="utf-8") as f:
        schema = json.load(f)
    data = json.loads(json_str)
    jsonschema.validate(data, schema)

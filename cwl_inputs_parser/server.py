#!/usr/bin/env python3
# coding: utf-8
from pathlib import Path
from traceback import format_exc
from typing import Tuple, Union

import yaml
from cwl_utils.parser import load_document_by_string
from flask import Blueprint, Flask, Response, jsonify, request

from cwl_inputs_parser.utils import Inputs, wf_location_to_inputs

app_bp = Blueprint("cwl-inputs-parser", __name__)


@app_bp.route("/", methods=["GET", "POST"])
def parse() -> Union[Tuple[Response, int], Tuple[Response, int]]:
    """
    Parse the inputs of a workflow.
    """
    req_data = yaml.safe_load(request.get_data().decode("utf-8"))
    wf_location = req_data.get("wf_location", None)
    wf_content = req_data.get("wf_content", None)
    if wf_location is None and wf_content is None:
        return jsonify({"message": "Missing arguments"}), 400
    if wf_location is not None:
        inputs = wf_location_to_inputs(wf_location.strip())
    elif wf_content is not None:
        wf_obj = load_document_by_string(wf_content, uri=Path.cwd().as_uri())  # noqa: E501
        inputs = Inputs(wf_obj)
    res = jsonify(inputs.as_dict())
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res, 200


def create_app() -> Flask:
    """
    Create the Flask app.
    """
    app = Flask(__name__)
    app.register_blueprint(app_bp)
    return app


def fix_errorhandler(app: Flask) -> Flask:
    @app.errorhandler(Exception)  # type: ignore
    def error_handler_exception(exception: Exception) -> Tuple[Response, int]:
        return jsonify({"message": f"The server encountered an internal error:\n{format_exc()}"}), 500  # noqa: E501

    return app

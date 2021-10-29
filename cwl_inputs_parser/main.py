#!/usr/bin/env python3
# coding: utf-8
import argparse
import sys

from cwl_inputs_parser.server import create_app
from cwl_inputs_parser.utils import wf_location_to_inputs


def arg_parser() -> argparse.ArgumentParser:
    """Generate argument parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "workflow_location",
        help="The location of workflow file (local path or remote URL)",
        default="",
        nargs="?"
    )
    parser.add_argument(
        "-s", "--server",
        help="Run in REST API server mode",
        action="store_true"
    )

    return parser


def main() -> None:
    """Main function."""
    parser = arg_parser()
    args = parser.parse_args()
    if args.server:
        app = create_app()
        app.run(host="0.0.0.0", port=8080, debug=True)
    else:
        if not args.workflow_location:
            print("[ERROR] The location of the workflow file is not specified.\n")  # noqa: E501
            parser.print_help()
            sys.exit(1)
        inputs = wf_location_to_inputs(args.workflow_location)
        print(inputs.as_json())


if __name__ == '__main__':
    main()
    sys.exit(0)

#!/usr/bin/env python3
# coding: utf-8
import argparse
import sys
from pathlib import Path

from cwl_utils.parser import load_document
from yaml import safe_load

from neko_punch.utils import CWLUtilLoadResult, fetch_document


def arg_parser() -> argparse.ArgumentParser:
    """Generate argument parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "workflow_file",
        help="The location of workflow file",
        default="workflows.yml",
        nargs="?"
    )

    return parser


def main() -> None:
    """Main function."""
    parser = arg_parser()
    args = parser.parse_args()
    workflow_file = Path(str(args.workflow_file))
    if not workflow_file.is_absolute():
        workflow_file = Path().cwd().joinpath(workflow_file)
    if workflow_file.exists() is False:
        print("[ERROR] workflow file not found")
        parser.print_help()
        sys.exit(1)

    with workflow_file.open(mode="r", encoding="utf-8") as f:
        workflows = safe_load(f)
    if "workflows" not in workflows or len(workflows["workflows"]) == 0:
        print("[ERROR] workflow file is empty")
        print("describe it as - workflows: [path, path, ...]")
        sys.exit(1)
    for wf_path in workflows["workflows"]:
        wf_doc = fetch_document(wf_path)
        cwl_obj: CWLUtilLoadResult = load_document(wf_doc)
        print(cwl_obj)


if __name__ == '__main__':
    main()
    sys.exit(0)

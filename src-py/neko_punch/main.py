#!/usr/bin/env python3
# coding: utf-8
import argparse
import sys
from pathlib import Path

from neko_punch.utils import wf_path_to_neko_fields
from yaml import safe_load


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
        neko_fields = wf_path_to_neko_fields(wf_path)
        print(neko_fields)


if __name__ == '__main__':
    main()
    sys.exit(0)

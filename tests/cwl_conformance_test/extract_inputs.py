# coding: utf-8
import sys

from cwl_utils.parser import load_document
from neko_punch.utils import fetch_document


def main():
    if len(sys.argv) != 2:
        print("Usage: extract_inputs.py <cwl_file_path>")
        sys.exit(1)
    cwl_file_path = sys.argv[1]
    cwl_obj = load_document(fetch_document(cwl_file_path))
    from pprint import pprint
    for input_obj in cwl_obj.inputs:
        pprint(input_obj.__dict__)
    pprint(cwl_obj.inputs[1].type.__dict__)


if __name__ == "__main__":
    main()

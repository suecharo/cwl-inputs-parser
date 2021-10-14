# coding: utf-8
import sys
from pprint import pprint

from cwl_utils.parser import load_document
from neko_punch.utils import fetch_document


def main():
    if len(sys.argv) != 2:
        print("Usage: extract_inputs.py <cwl_file_path>")
        sys.exit(1)
    cwl_file_path = sys.argv[1]
    cwl_obj = load_document(fetch_document(cwl_file_path))
    for input_obj in cwl_obj.inputs:
        pprint(input_obj.__dict__)
        if input_obj.secondaryFiles:
            print("secondaryFiles:")
            for secondary_file in input_obj.secondaryFiles:
                pprint(secondary_file.__dict__)


if __name__ == "__main__":
    main()

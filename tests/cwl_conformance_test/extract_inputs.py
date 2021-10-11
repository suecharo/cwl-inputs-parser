# coding: utf-8
import sys
from pathlib import Path

from cwl_utils.parser import load_document
from requests import get


def is_remote_url(path):
    return path.startswith("http")


def main():
    if len(sys.argv) != 2:
        print("Usage: extract_inputs.py <cwl_file_url>")
        sys.exit(1)
    file_url = sys.argv[1]
    file_string = ""
    if is_remote_url(file_url):
        res = get(file_url)
        if res.status_code != 200:
            print("Failed to download file")
            sys.exit(1)
        file_string = res.text
    else:
        file_url = Path(file_url).absolute()
        with file_url.open("r") as f:
            file_string = f.read()
    print(file_string)
    cwl_obj = load_document(file_string)
    from pprint import pprint
    for input_obj in cwl_obj.inputs:
        pprint(input_obj.__dict__)
    pprint(cwl_obj.inputs[1].type.__dict__)


if __name__ == "__main__":
    main()

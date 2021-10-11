#!/usr/bin/env python3
# coding: utf-8
import sys

import argcomplete
from cwltool.context import RuntimeContext
from cwltool.main import (arg_parser, fetch_document, get_default_args,
                          make_template, make_tool,
                          resolve_and_validate_document, resolve_tool_uri,
                          setup_loadingContext)


def main():
    if len(sys.argv) != 2:
        print("Usage: cwltool_make_template.py <cwl_file_url>")
        sys.exit(1)
    cwl_file_url = sys.argv[1]
    parser = arg_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args(["--make-template", cwl_file_url])
    for key, val in get_default_args().items():
        if not hasattr(args, key):
            setattr(args, key, val)
    runtimeContext = RuntimeContext(vars(args))
    loadingContext = setup_loadingContext(None, runtimeContext, args)
    uri, _ = resolve_tool_uri(
        args.workflow,
        resolver=loadingContext.resolver,
        fetcher_constructor=loadingContext.fetcher_constructor,
    )
    loadingContext, workflowobj, uri = fetch_document(uri, loadingContext)
    loadingContext, uri = resolve_and_validate_document(
        loadingContext,
        workflowobj,
        uri,
        preprocess_only=(args.print_pre or args.pack),
        skip_schemas=args.skip_schemas,
    )
    tool = make_tool(uri, loadingContext)
    make_template(tool)


if __name__ == "__main__":
    main()

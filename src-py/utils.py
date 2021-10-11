#!/usr/bin/env python3
# coding: utf-8
from requests import get


def download_file(url):
    """Downloads a file from a URL and returns the content."""
    response = get(url)
    if response.status_code != 200:
        raise Exception("Failed to download file: {}".format(url))
    return response.text


def cwl_make_template(cwl_file_url):
    """Returns the results of cwltool --make-template."""
    import logging

    from cwltool.main import (RuntimeContext, arg_parser, argcomplete,
                              fetch_document, generate_input_template,
                              get_default_args, make_tool,
                              resolve_and_validate_document, resolve_tool_uri,
                              setup_loadingContext)

    logging.getLogger("cwltool").setLevel(logging.ERROR)
    logging.getLogger("salad").setLevel(logging.ERROR)

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
    )
    return generate_input_template(make_tool(uri, loadingContext))

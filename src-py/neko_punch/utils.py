#!/usr/bin/env python3
# coding: utf-8
from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional, Union, cast

from cwl_utils.parser.cwl_v1_2 import (CommandInputParameter, CommandLineTool,
                                       ExpressionTool, Workflow)
from cwltool.main import CWLObjectType
from requests import get

CWLUtilObj = Union[CommandLineTool, Workflow, ExpressionTool]
CWLUtilLoadResult = Union[List[CWLUtilObj], CWLUtilObj]


def download_file(remote_url: str) -> str:
    """Downloads a file from a URL and returns the content."""
    response = get(remote_url)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: {remote_url}")
    return response.text


def cwl_make_template(path: str) -> CWLObjectType:
    """Returns the results of cwltool --make-template."""
    import logging

    from cwltool.main import RuntimeContext, arg_parser, argcomplete
    from cwltool.main import fetch_document as cwltool_fetch_document
    from cwltool.main import (generate_input_template, get_default_args,
                              make_tool, resolve_and_validate_document,
                              resolve_tool_uri, setup_loadingContext)

    logging.getLogger("cwltool").setLevel(logging.ERROR)
    logging.getLogger("salad").setLevel(logging.ERROR)

    parser = arg_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args(["--make-template", path])
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
    loadingContext, workflowobj, uri = cwltool_fetch_document(
        uri,
        loadingContext
    )
    loadingContext, uri = resolve_and_validate_document(
        loadingContext,
        workflowobj,
        uri,
    )
    return generate_input_template(make_tool(uri, loadingContext))


def is_remote_url(path: str) -> bool:
    """Returns True if the path is a remote URL."""
    return path.startswith("http://") or path.startswith("https://")


def fetch_document(path: Union[str, Path]) -> str:
    """Fetches a CWL document from a file or URL."""
    if isinstance(path, str):
        if is_remote_url(path):
            return download_file(path)
        path = Path(path)
    if path.is_absolute():
        return path.open(mode="r", encoding="utf-8").read()
    else:
        return Path().cwd().joinpath(path).read_text(encoding="utf-8")


def extract_main_tool(cwl_obj: CWLUtilLoadResult) -> CWLUtilObj:
    """Extracts the main tool from a CWL object."""
    if isinstance(cwl_obj, list):
        for obj in cwl_obj:
            if obj.class_ == "Workflow" or str(obj.id).split("#")[-1] == "main":  # noqa: E501
                return obj
    return cast(CWLUtilObj, cwl_obj)


@dataclass
class NekoField:
    """NekoField"""
    default: Optional[Any] = None
    doc: Optional[str] = None
    id: Optional[str] = None
    label: Optional[str] = None
    type: Optional[str] = None


class Neko:
    """Generates NekoFields from a cwl-utils object."""
    def __init__(self, cwl_obj: CWLUtilLoadResult) -> None:
        self.ori_cwl_obj = deepcopy(cwl_obj)
        self.cwl_obj = deepcopy(extract_main_tool(cwl_obj))
        self.results: List[NekoField] = []

    def punch(self):
        """Converts a CWL object to a Neko object."""
        for inp_obj in self.cwl_obj.inputs:
            if isinstance(inp_obj, str):
                if inp_obj.type == "boolean":
                    self.results.append(self.boolean_field(inp_obj))
                elif inp_obj.type == "int":
                    self.results.append(self.int_field(inp_obj))
                elif inp_obj.type == "string":
                    self.results.append(self.string_field(inp_obj))
                elif inp_obj.type == "File":
                    self.results.append(self.file_field(inp_obj))
                elif inp_obj.type == "stdin":
                    self.results.append(self.stdin_field(inp_obj))
                elif inp_obj.type == "Directory":
                    self.results.append(self.directory_field(inp_obj))
                elif inp_obj.type == "Any":
                    self.results.append(self.any_field(inp_obj))
            elif isinstance(inp_obj, list):
                pass

    @staticmethod
    def clean_val(val: Optional[Any]) -> Optional[Any]:
        """Cleans a value."""
        if val is None:
            return None
        elif isinstance(val, str):
            return deepcopy(val).replace("\n", " ").strip()
        return deepcopy(val)

    def template_field(self, inp_obj: CommandInputParameter) -> NekoField:
        """Generates a NekoField template from a CWL InputParameter."""
        id_ = self.clean_val(inp_obj.id)
        if isinstance(id_, str):
            id_ = id_.split("#")[-1]
        return NekoField(
            default=deepcopy(inp_obj),
            doc=self.clean_val(inp_obj.doc),
            id=id_,
            label=self.clean_val(inp_obj.label),
            type=self.clean_val(inp_obj.type),
        )

    def boolean_field(self, inp_obj: CommandInputParameter) -> NekoField:
        """
        Generates a NekoField from a CWL InputParameter.
        inp_obj example:
        {
            'default': True,
            'doc': 'If true, reverse (decending) sort',
            'extension_fields': ordereddict(),
            'format': None,
            'id': 'file:///app/tests/cwl_conformance_test/#reverse_sort',
            'inputBinding': None,
            'label': None,
            'loadContents': None,
            'loadListing': None,
            'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7f7860454520>, # noqa: E501
            'secondaryFiles': None,
            'streamable': None,
            'type': 'boolean'
        }
        """
        return self.template_field(inp_obj)

    def int_field(self, inp_obj: CommandInputParameter) -> NekoField:
        """
        Generates a NekoField from a CWL InputParameter.
        inp_obj example:
        {
            'default': None,
            'doc': None,
            'extension_fields': ordereddict(),
            'format': None,
            'id': 'file:///app/tests/cwl_conformance_test/#minimum_seed_length',  # noqa: E501
            'inputBinding': <cwl_utils.parser.cwl_v1_2.CommandLineBinding object at 0x7f0fa553c220>,  # noqa: E501
            'label': None,
            'loadContents': None,
            'loadListing': None,
            'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7f0fa757a7f0>,  # noqa: E501
            'secondaryFiles': None,
            'streamable': None,
            'type': 'int'
        }
        """
        return self.template_field(inp_obj)

    def string_field(self, inp_obj: CommandInputParameter) -> NekoField:
        """
        Generates a NekoField from a CWL InputParameter.
        inp_obj example:
        {
            'default': 'hello inp1',
            'doc': None,
            'extension_fields': ordereddict(),
            'format': None,
            'id': 'file:///app/tests/cwl_conformance_test/#inp1',
            'inputBinding': None,
            'label': None,
            'loadContents': None,
            'loadListing': None,
            'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7f930c01b370>,  # noqa: E501
            'secondaryFiles': None,
            'streamable': None,
            'type': 'string'
        }
        """
        return self.template_field(inp_obj)

    def file_field(self, inp_obj: CommandInputParameter) -> NekoField:
        """
        Generates a NekoField from a CWL InputParameter.
        inp_obj example:
        {
            'default': ordereddict([('class', 'File'), ('path', 'whale.txt')]),
            'doc': None,
            'extension_fields': ordereddict(),
            'format': None,
            'id': 'file:///app/tests/cwl_conformance_test/#file1',
            'inputBinding': None,
            'label': None,
            'loadContents': None,
            'loadListing': None,
            'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7fe155efc790>,  # noqa: E501
            'secondaryFiles': None,
            'streamable': None,
            'type': 'File'
        }

        default における path と location は基本的に全部 location と考えて良い
        > As a special case, if the path field is provided but the
        location field is not, an implementation may assign the value
        of the path field to location, and remove the path field.
        """
        result = self.template_field(inp_obj)
        default = None
        if isinstance(inp_obj.default, OrderedDict) and len(inp_obj.default) != 0:  # noqa: E501
            if "location" in inp_obj.default:
                default = inp_obj.default["location"]
            elif "path" in inp_obj.default:
                default = inp_obj.default["path"]
        result.default = default
        return result

    def stdin_field(self, inp_obj: CommandInputParameter) -> NekoField:
        """
        Generates a NekoField from a CWL InputParameter.
        example:
        {
            'default': None,
            'doc': None,
            'extension_fields': ordereddict(),
            'format': None,
            'id': 'file:///app/tests/cwl_conformance_test/#file1',
            'inputBinding': None,
            'label': None,
            'loadContents': None,
            'loadListing': None,
            'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7f4910221e80>,  # noqa: E501
            'secondaryFiles': None,
            'streamable': None,
            'type': 'stdin'
        }
        """
        result = self.file_field(inp_obj)
        result.type = "File"
        return result

    def directory_field(self, inp_obj: CommandInputParameter) -> NekoField:
        """
        Generates a NekoField from a CWL InputParameter.
        example:
        {
            'default': None,
            'doc': None,
            'extension_fields': ordereddict(),
            'format': None,
            'id': 'file:///app/tests/cwl_conformance_test/#indir',
            'inputBinding': None,
            'label': None,
            'loadContents': None,
            'loadListing': 'shallow_listing',
            'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7f975ee99a60>,  # noqa: E501
            'secondaryFiles': None,
            'streamable': None,
            'type': 'Directory'
        }
        """
        return self.template_field(inp_obj)

    def any_field(self, inp_obj: CommandInputParameter) -> NekoField:
        """
        Generates a NekoField from a CWL InputParameter.
        example:
        {
            'default': 'the-default',
            'doc': None,
            'extension_fields': ordereddict(),
            'format': None,
            'id': 'file:///app/tests/cwl_conformance_test/#i1',
            'inputBinding': None,
            'label': None,
            'loadContents': None,
            'loadListing': None,
            'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7ff803637220>,  # noqa: E501
            'secondaryFiles': None,
            'streamable': None,
            'type': 'Any'
        }
        """
        return self.template_field(inp_obj)

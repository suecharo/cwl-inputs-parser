#!/usr/bin/env python3
# coding: utf-8
from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, NoReturn, Optional, Union, cast
import os


from cwl_utils.parser import load_document
from cwl_utils.parser.cwl_v1_2 import (CommandInputArraySchema,
                                       CommandInputEnumSchema,
                                       CommandInputParameter,
                                       CommandInputRecordSchema,
                                       CommandLineTool, ExpressionTool,
                                       InputArraySchema, InputRecordSchema,
                                       Workflow, file_uri)
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


def as_uri(path: Union[str, Path]) -> str:
    """Converts a path to a URI."""
    if isinstance(path, str):
        if is_remote_url(path):
            return os.path.dirname(path) + "/"
        path = Path(path)
    if not path.is_absolute():
        path = Path().cwd().joinpath(path)
    return file_uri(str(path.parent)) + "/"


def extract_main_tool(cwl_obj: CWLUtilLoadResult) -> CWLUtilObj:
    """Extracts the main tool from a CWL object."""
    if isinstance(cwl_obj, list):
        for obj in cwl_obj:
            if obj.class_ == "Workflow" or str(obj.id).rsplit("#", maxsplit=1)[-1] == "main":  # noqa: E501
                return obj
    return cast(CWLUtilObj, cwl_obj)


class UnsupportedValueError(Exception):
    """Raised when an unsupported value is encountered."""


@dataclass
class SecondaryFile:
    """SecondaryFile"""
    pattern: Optional[str] = None
    required: Optional[bool] = True


@dataclass
class NekoField:
    """
    NekoField
    example:
    {
        "default": null,
        "doc": "doc example",
        "id": "id example",
        "label": "label example",
        "type": "File",
        "required": true,
        "secondaryFiles": [
            {
                "pattern": "pattern example",
                "required": true,
            }
        ],
    }
    """
    default: Optional[Any] = None
    doc: Optional[str] = None
    id: Optional[str] = None
    label: Optional[str] = None
    type: Optional[str] = None
    array: bool = False
    required: bool = True
    secondaryFiles: Optional[List[SecondaryFile]] = None


class Neko:
    """Generates NekoFields from a cwl-utils object."""
    def __init__(self, cwl_obj: CWLUtilLoadResult) -> None:
        self.ori_cwl_obj = deepcopy(cwl_obj)
        self.cwl_obj = deepcopy(extract_main_tool(cwl_obj))
        self.results: List[NekoField] = []

    def punch(self):
        """Converts a CWL object to a Neko object."""
        for inp_obj in self.cwl_obj.inputs:
            if isinstance(inp_obj.type, str):
                self.results.append(self.typical_field(inp_obj))
            elif isinstance(inp_obj.type, list):
                if len(inp_obj.type) == 1:
                    tmp_obj = deepcopy(inp_obj)
                    tmp_obj.type = inp_obj.type[0]
                    if isinstance(tmp_obj.type, str):
                        self.results.append(self.typical_field(tmp_obj))
                    elif isinstance(tmp_obj.type, CommandInputArraySchema):
                        self.results.append(self.command_input_array_field(tmp_obj))  # noqa: E501
                    elif isinstance(tmp_obj.type, InputArraySchema):
                        self.results.append(self.input_array_field(tmp_obj))
                    else:
                        raise UnsupportedValueError("The type field contains an unsupported format")  # noqa: E501
                elif len(inp_obj.type) == 2:
                    if 'null' in inp_obj.type:
                        tmp_obj = deepcopy(inp_obj)
                        for t in inp_obj.type:
                            if t != 'null':
                                tmp_obj.type = t
                        neko_filed = self.typical_field(tmp_obj)
                        neko_filed.required = False
                        self.results.append(neko_filed)
                    else:
                        # [TODO] not support
                        raise UnsupportedValueError("The union field does not support by neko-punch")  # noqa: E501
                else:
                    # [TODO] not support
                    raise UnsupportedValueError("The union field does not support by neko-punch")  # noqa: E501
            elif isinstance(inp_obj.type, CommandInputArraySchema):
                if inp_obj.type.items not in ["boolean", "int", "string", "File", "Directory", "Any"]:  # noqa: E501
                    raise UnsupportedValueError("The type field contains an unsupported format")  # noqa: E501
                self.results.append(self.command_input_array_field(inp_obj))
            elif isinstance(inp_obj.type, CommandInputEnumSchema):
                # [TODO] not support
                # self.results.append(self.command_input_enum_field(inp_obj))
                raise UnsupportedValueError("The CommandInputEnumSchema field does not support by neko-punch")  # noqa: E501
            elif isinstance(inp_obj.type, CommandInputRecordSchema):
                # [TODO] not support
                # self.results.append(self.command_input_record_field(inp_obj))
                raise UnsupportedValueError("The CommandInputRecordSchema field does not support by neko-punch")  # noqa: E501
            elif isinstance(inp_obj.type, InputArraySchema):
                if isinstance(inp_obj.type.items, InputRecordSchema):
                    # [TODO] not support
                    raise UnsupportedValueError("The InputRecordSchema field in the InputArraySchema field does not support by neko-punch")  # noqa: E501
                if inp_obj.type.items not in ["boolean", "int", "string", "File", "Directory", "Any"]:  # noqa: E501
                    raise UnsupportedValueError("The type field contains an unsupported format")  # noqa: E501
                self.results.append(self.input_array_field(inp_obj))
            elif isinstance(inp_obj.type, InputRecordSchema):
                # [TODO] not support
                raise UnsupportedValueError("The InputRecordSchema field does not support by neko-punch")  # noqa: E501
            else:
                # [TODO] not support
                raise UnsupportedValueError("The type field contains an unsupported format")  # noqa: E501

    def typical_field(self, inp_obj: CommandInputParameter) -> NekoField:
        """
        Generates a typical fields
        like: boolean, int, string, File, stdin, Directory, Any
        """
        if inp_obj.type == "boolean":
            return self.boolean_field(inp_obj)
        elif inp_obj.type == "int":
            return self.int_field(inp_obj)
        elif inp_obj.type == "string":
            return self.string_field(inp_obj)
        elif inp_obj.type == "File":
            return self.file_field(inp_obj)
        elif inp_obj.type == "stdin":
            return self.stdin_field(inp_obj)
        elif inp_obj.type == "Directory":
            return self.directory_field(inp_obj)
        elif inp_obj.type == "Any":
            return self.any_field(inp_obj)
        else:
            # [TODO] not support
            raise UnsupportedValueError("The type field contains an unsupported format")  # noqa: E501

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
            default=deepcopy(inp_obj.default),
            doc=self.clean_val(inp_obj.doc),
            id=id_,
            label=self.clean_val(inp_obj.label),
            type=self.clean_val(inp_obj.type),
        )

    def boolean_field(self, inp_obj: CommandInputParameter) -> NekoField:
        """
        Generates a NekoField from a CWL InputParameter.
        inp_obj example from 'v1.2/revsort-packed.cwl'
        {
            'default': True,
            'doc': 'If true, reverse (decending) sort',
            'extension_fields': ordereddict(),
            'format': None,
            'id': 'file:///app/tests/cwl_conformance_test/#main/reverse_sort',
            'inputBinding': None,
            'label': None,
            'loadContents': None,
            'loadListing': None,
            'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7feb232f7be0>,  # noqa: E501
            'secondaryFiles': None,
            'streamable': None,
            'type': 'boolean'
        }
        make-template result:
        reverse_sort: true  # default value of type "boolean".
        """
        return self.template_field(inp_obj)

    def int_field(self, inp_obj: CommandInputParameter) -> NekoField:
        """
        Generates a NekoField from a CWL InputParameter.
        inp_obj example from 'v1.2/bwa-mem-tool.cwl'
        {
            'default': None,
            'doc': None,
            'extension_fields': ordereddict(),
            'format': None,
            'id': 'file:///app/tests/cwl_conformance_test/#minimum_seed_length',  # noqa: E501
            'inputBinding': <cwl_utils.parser.cwl_v1_2.CommandLineBinding object at 0x7f3c1af41220>, # noqa: E501
            'label': None,
            'loadContents': None,
            'loadListing': None,
            'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7f3c1cdec730>,  # noqa: E501
            'secondaryFiles': None,
            'streamable': None,
            'type': 'int'
        }
        make-template result:
        minimum_seed_length: 0  # type "int"
        """
        return self.template_field(inp_obj)

    def string_field(self, inp_obj: CommandInputParameter) -> NekoField:
        """
        Generates a NekoField from a CWL InputParameter.
        inp_obj example from 'v1.2/pass-unconnected.cwl'
        {
            'default': 'hello inp2',
            'doc': None,
            'extension_fields': ordereddict(),
            'format': None,
            'id': 'file:///app/tests/cwl_conformance_test/#inp2',
            'inputBinding': None,
            'label': None,
            'loadContents': None,
            'loadListing': None,
            'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7fd904cfe370>,  # noqa: E501
            'secondaryFiles': None,
            'streamable': None,
            'type': 'string'
        }
        make-template result:
        inp2: hello inp2  # default value of type "string".
        """
        return self.template_field(inp_obj)

    def file_field(self, inp_obj: CommandInputParameter) -> NekoField:
        """
        Generates a NekoField from a CWL InputParameter.
        inp_obj example from 'v1.2/count-lines5-wf.cwl'
        {
            'default': ordereddict([('class', 'File'), ('location', 'hello.txt')]),
            'doc': None,
            'extension_fields': ordereddict(),
            'format': None,
            'id': 'file:///app/tests/cwl_conformance_test/#file1',
            'inputBinding': None,
            'label': None,
            'loadContents': None,
            'loadListing': None,
            'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7fa708c4b0d0>,  # noqa: E501
            'secondaryFiles': None,
            'streamable': None,
            'type': 'File'
        }
        make-template result:
        file1: {class: File, location: file:///app/tests/cwl_conformance_test/v1.2/hello.txt}  # default value of type "File".

        Basically, all path and location can be treated as location.
        > As a special case, if the path field is provided but the
        location field is not, an implementation may assign the value
        of the path field to location, and remove the path field.
        """
        result = self.template_field(inp_obj)
        if isinstance(inp_obj.default, OrderedDict) and len(inp_obj.default) != 0:  # noqa: E501
            if "location" in inp_obj.default:
                result.default = inp_obj.default["location"]
            elif "path" in inp_obj.default:
                result.default = inp_obj.default["path"]
        return result

    def stdin_field(self, inp_obj: CommandInputParameter) -> NekoField:
        """
        Generates a NekoField from a CWL InputParameter.
        inp_obj example from 'v1.2/cat-tool-shortcut.cwl'
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
            'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7f3f40a59d60>,  # noqa: E501
            'secondaryFiles': None,
            'streamable': None,
            'type': 'stdin'
        }
        make-template result:
        file1:  # type "File"
            class: File
            path: a/file/path
        """
        result = self.file_field(inp_obj)
        result.type = "File"
        return result

    def directory_field(self, inp_obj: CommandInputParameter) -> NekoField:
        """
        Generates a NekoField from a CWL InputParameter.
        inp_obj example from 'v1.2/dir.cwl'
        {
            'default': None,
            'doc': None,
            'extension_fields': ordereddict(),
            'format': None,
            'id': 'file:///app/tests/cwl_conformance_test/#indir',
            'inputBinding': None,
            'label': None,
            'loadContents': None,
            'loadListing': None,
            'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7f44a93efca0>,  # noqa: E501
            'secondaryFiles': None,
            'streamable': None,
            'type': 'Directory'
        }
        make-template result:
        indir:  # type "Directory"
            class: Directory
            path: a/directory/path
        """
        return self.template_field(inp_obj)

    def any_field(self, inp_obj: CommandInputParameter) -> NekoField:
        """
        Generates a NekoField from a CWL InputParameter.
        inp_obj example from 'v1.2/null-expression1-tool.cwl'
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
            'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7f8774eba220>,  # noqa: E501
            'secondaryFiles': None,
            'streamable': None,
            'type': 'Any'
        }
        make-template result:
        i1: "the-default"  # default value of type "Any".
        """
        return self.template_field(inp_obj)

    def command_input_array_field(self, inp_obj: CommandInputParameter) -> NekoField:  # noqa: E501
        """
        Generates a NekoField from a CWL InputParameter.
        [TODO] more check
        inp_obj example from 'v1.2/docker-array-secondaryfiles.cwl'
        {
            'default': None,
            'doc': None,
            'extension_fields': ordereddict(),
            'format': None,
            'id': 'file:///app/tests/cwl_conformance_test/#fasta_path',
            'inputBinding': None,
            'label': None,
            'loadContents': None,
            'loadListing': None,
            'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7fd3104d2130>,  # noqa: E501
            'secondaryFiles': [<cwl_utils.parser.cwl_v1_2.SecondaryFileSchema object at 0x7fd3104e27c0>,  # noqa: E501
                                <cwl_utils.parser.cwl_v1_2.SecondaryFileSchema object at 0x7fd3104e2940>,  # noqa: E501
                                <cwl_utils.parser.cwl_v1_2.SecondaryFileSchema object at 0x7fd3104e2a60>],  # noqa: E501
            'streamable': None,
            'type': <cwl_utils.parser.cwl_v1_2.CommandInputArraySchema object at 0x7fd3104e2dc0>
        }

        make-template result:
        require_dat: false  # type "boolean" (optional)
        fasta_path:  # array of type "File"
        - class: File
            path: a/file/path

        secondaryFiles:
        {'extension_fields': ordereddict(),
        'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7f634a456460>,
        'pattern': '.bai',
        'required': False}
        {'extension_fields': ordereddict(),
        'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7f634a456460>,
        'pattern': "${ if (inputs.require_dat) {return '.dat'} else {return null} }",
        'required': None}
        {'extension_fields': ordereddict(),
        'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7f634a456460>,
        'pattern': '${ return null; }',
        'required': None}
        """
        result = self.template_field(inp_obj)
        result.type = inp_obj.type.items
        result.array = True
        if inp_obj.secondaryFiles:
            result.secondaryFiles = []
            for secondary_file in inp_obj.secondaryFiles:
                result.secondaryFiles.append(
                    SecondaryFile(
                        pattern=secondary_file.pattern,
                        required=secondary_file.required
                    )
                )
        return result

    def command_input_enum_field(self, inp_obj: CommandInputParameter) -> NoReturn:  # noqa: E501
        """
        Generates a NekoField from a CWL InputParameter.

        [TODO] do not know how to handle enum field in CWL, therefore
        the neko-punch will not support this.
        """

    def command_input_record_field(self, inp_obj: CommandInputParameter) -> NoReturn:  # noqa: E501
        """
        Generates a NekoField from a CWL InputParameter.
        v1.2/record-output.cwl
        v1.2/anon_enum_inside_array.cwl
        v1.2/record-in-secondaryFiles.cwl
        v1.2/record-in-format.cwl
        v1.2/record-out-format.cwl

        [TODO] do not know how to handle record field in CWL, therefore
        the neko-punch will not support this.
        """

    def input_array_field(self, inp_obj: CommandInputParameter) -> NekoField:
        """
        Generates a NekoField from a CWL InputParameter.
        inp_obj example from 'v1.2/count-lines3-wf.cwl'
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
            'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7f26ca1b2160>,  # noqa: E501
            'secondaryFiles': None,
            'streamable': None,
            'type': <cwl_utils.parser.cwl_v1_2.InputArraySchema object at 0x7f26ca1422e0>
        }
        type:
        {
            'doc': None,
            'extension_fields': ordereddict(),
            'items': 'File',
            'label': None,
            'loadingOptions': <cwl_utils.parser.cwl_v1_2.LoadingOptions object at 0x7f26ca1b2160>,
            'name': '_:7db2ff08-5fed-4261-b514-fe5eccc43048',
            'type': 'array'
        }

        make-template result:
        file1:  # array of type "File"
            - class: File
                path: a/file/path
        """
        result = self.template_field(inp_obj)
        result.type = inp_obj.type.items
        result.array = True
        if result.label is None:
            result.label = self.clean_val(inp_obj.type.label)
        if result.doc is None:
            result.doc = self.clean_val(inp_obj.type.doc)
        return result


def wf_path_to_neko_fields(wf_path: str) -> List[NekoField]:
    """Convert workflow path to neko object."""
    wf_doc = fetch_document(wf_path)
    cwl_obj: CWLUtilLoadResult = load_document(wf_doc, baseuri=as_uri(wf_path))
    neko = Neko(cwl_obj)
    neko.punch()
    return neko.results

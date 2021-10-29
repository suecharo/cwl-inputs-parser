# cwl-inputs-parser

A library for parsing the inputs field of Common Workflow Language (CWL) document.
This library aims to use it as a CWL parser to generate a web form to execute the Workflow Execution Service (WES).

As a simple example, if you input [tests/all_input.cwl](https://github.com/suecharo/cwl-inputs-parser/blob/main/tests/all_input.cwl), [tests/all_input.json](https://github.com/suecharo/cwl-inputs-parser/blob/main/tests/all_input.json) will be output.

The schema of the parsed results is [cwl-inputs-parser-schema.json](https://github.com/suecharo/cwl-inputs-parser/blob/main/cwl-inputs-parser-schema.json).

We are testing using the CWL v1.2 conformance test.
The list of test IDs that will not pass is [tests/cwl_conformance_test/failed_test_ids.txt](https://github.com/suecharo/cwl-inputs-parser/blob/main/tests/cwl_conformance_test/failed_test_ids.txt).

## Installation

Requires Python 3.6+

To install from PyPI:

```bash
$ pip install cwl-inputs-parser
$ cwl-inputs-parser --help
```

To install from source:

```bash
$ git clone https://github.com/suecharo/cwl-inputs-parser.git
$ cd cwl-inputs-parser
$ pip install .
$ cwl-inputs-parser --help
```

To install with docker:

```bash
$ docker run -t --rm ghcr.io/suecharo/cwl-inputs-parser:latest --help
```

## Usage

### As command line tool

Use as a command line tool:

```bash
$ cwl-inputs-parser /path/to/cwl_document (local file path | remote URL)
```

### As REST API server

Start the server:

```bash
$ cwl-inputs-parser -s
 * Serving Flask app 'cwl_inputs_parser.server' (lazy loading)
 * Environment: production
 * Debug mode: off
 * Running on http://172.26.0.2:8080/ (Press CTRL+C to quit)
```

Request with `curl`:

```bash
# {"wf_location": "https://path/to/workflow"}
$ curl -X POST localhost:8080 -d @tests/curl_data_location.json
...

# {"wf_content": "serialized CWL contents..."}
$ curl -X POST localhost:8080 -d @tests/curl_data_content.json
...

$ curl -X POST \
  localhost:8080 \
  -d '{"wf_location": "https://raw.githubusercontent.com/suecharo/cwl-inputs-parser/main/tests/cwl_conformance_test/v1.2/wc-tool.cwl"}'
[{"array":false,"default":null,"doc":null,"id":"file1","label":null,"required":true,"secondaryFiles":null,"type":"File"}]
```

### As python library

Use as a python library:

```bash
$ python3
Python 3.8.12 (default, Oct 13 2021, 13:56:21)
[GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from cwl_inputs_parser.utils import wf_location_to_inputs
>>> inputs = wf_location_to_inputs("./tests/cwl_conformance_test/v1.2/wc-tool.cwl")
>>> inputs.as_dict()
[{'default': None, 'doc': None, 'id': 'file1', 'label': None, 'type': 'File', 'array': False, 'required': True, 'secondaryFiles': None}]
```

## Development

development environment:

```bash
docker-compose -f docker-compose.dev.yml up -d --build
docker-compose -f docker-compose.dev.yml exec app bash
```

testing:

```bash
pytest .
```

## License

[Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
See the [LICENSE](https://github.com/suecharo/cwl-inputs-parser/blob/main/LICENSE).

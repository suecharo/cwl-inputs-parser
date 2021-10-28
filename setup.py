#!/usr/bin/env python3
# coding: utf-8
from pathlib import Path

from setuptools import setup

with Path(__file__).parent.joinpath("README.md").open(mode="r", encoding="utf-8") as f:  # noqa: E501
    long_description = f.read()

setup(
    name="cwl-inputs-parser",
    version="0.1.0",
    license="Apache 2.0",
    description="The parser of inputs field in Common Workflow Language (CWL)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="suecharo",
    author_email="suehiro619@gmail.com",
    url="https://github.com/suecharo/neko-punch",
    python_requires=">=3.6",
    install_requires=[
        "cwl-utils @ git+https://github.com/common-workflow-language/cwl-utils.git@d5e0338b7fbeb93f2872f9e2268a4af7e092a57b",  # noqa
        "flask",
        "pyyaml",
        "requests",
    ],
    extras_require={
        "testing": [
            "isort",
            "jsonschema",
            "mypy",
            "pytest",
            "types-PyYAML",
            "types-requests",
            "types-setuptools",
        ],
    },
    packages=["cwl_inputs_parser"],
    entry_points={
        "console_scripts": [
            "cwl-inputs-parser=cwl_inputs_parser.main:main",
        ]
    },
)

#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup

setup(
    name="neko-punch",
    version="0.1",
    license="Apache 2.0",
    description="Light-weight web component for workflow execution service",
    long_description=open("./README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="suecharo",
    author_email="suehiro619@gmail.com",
    url="https://github.com/suecharo/neko-punch",
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "cwltool",
        "cwl-utils @ git+https://github.com/common-workflow-language/cwl-utils.git@d5e0338b7fbeb93f2872f9e2268a4af7e092a57b",  # noqa
        "pyyaml",
        "requests",
    ],
    extras_require={
        "testing": [
            "mypy",
            "types-PyYAML",
            "types-requests",
            "types-setuptools",
            "isort",
            "pytest",
            "jsonschema",
        ],
    },
    packages=["neko_punch"],
    package_dir={
        "": "src-py",
    },
    entry_points={
        "console_scripts": [
            "neko-punch=neko_punch.main:main",
        ]
    },
)

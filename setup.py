#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup

setup(
    name="neko_punch",
    version="0.1",
    license="Apache 2.0",
    description="Light-weight web component for workflow execution service",
    long_description=open("./README.md").read(),
    long_description_content_type="text/markdown",
    author="suecharo",
    author_email="suehiro619@gmail.com",
    url="https://github.com/suecharo/neko-punch",
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "cwltool",
        "cwl-utils @ git@github.com:common-workflow-language/cwl-utils@8cc5de7305c1a445a5e61e5373cfa44917366d7c",  # noqa: E501
        "pyyaml",
        "requests",
    ],
    packages=["neko_punch", "neko_punch.tests"],
    package_dir={
        "neko_punch": "src-py",
        "neko_punch.tests": "tests",
    },
)

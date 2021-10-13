#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup

setup(
    name="neko-punch",
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
        # "cwl-utils",  # not working
        "pyyaml",
        "requests",
    ],
    packages=["neko_punch"],
    package_dir={
        "": "src-py",
    },
)

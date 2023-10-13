#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import setuptools

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

setuptools.setup(
    name="nsq2arangodb",
    version="1.0.1",
    author="Lars Wallenborn",
    description="data transportation from NSQ to ArangoDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/larsborn/nsq2arangodb",
    project_urls={
        "Bug Tracker": "https://github.com/larsborn/nsq2arangodb/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)

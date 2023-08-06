#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : aidenmo
# @Email : aidenmo@tencent.com
# @Time : 2021/8/22 13:34
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="reproxy",
    version="1.0.0",
    author="aidenmo",
    author_email="aidenmo@tencent.com",
    description="proxy request pass by redis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="proxy, requests",
    url="",
    packages=['reproxy'],
    install_requires=['requests', 'redis'],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
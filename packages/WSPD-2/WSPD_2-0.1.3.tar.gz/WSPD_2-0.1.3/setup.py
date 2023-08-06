# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 11:18:26 2023

@author: Sören 
"""

import os
# from setuptools import find_packages, setup
import setuptools

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

setuptools.setup(
    name="WSPD_2",
    version='0.1.3',
    author="Domagoj Matijevic",
    author_email="dmatijev@mathos.hr",
    description="The WSPD_2 Python package",
    long_description="Computes a well-separated pairs decomposition.",
    long_description_content_type="text/markdown",
    url="https://github.com/dmatijev/wspd_2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

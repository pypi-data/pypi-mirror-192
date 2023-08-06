#!/usr/bin/env python

import setuptools

description = """
A tool to display categories and subcategories based on hand-crafted predicates
and show the corresponding Sankey diagrams.
"""


setuptools.setup(
    name='simple-categorisation',
    version='0.1',
    description=description,
    author='JB Robertson',
    author_email='jbr@freeshell.org',
    url='https://sr.ht/~jbrobertson/simple-categorisation/',
    packages=['simple_categorisation'],
    install_requires=[],
    extras_require={
        "dev": [
            "flake8==3.8.4",
            "mock==4.0.3",
            "pytest-cov==2.10.1",
        ]
    },
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ])

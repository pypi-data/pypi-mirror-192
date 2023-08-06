#!/usr/bin/env python

import setuptools

description = """
A tool to display categories and subcategories based on hand-crafted predicates
and show the corresponding Sankey diagrams.
"""

long_description = """
# Simple categorisation

Define categories and sub-categories with predicates, and categorise
lists of items based on these categories:

```python
cat = Categoriser()
# The category of items that are < 0.5
cat.add("x < 0.5", lambda x: x < 0.5)
# Items over 1
over_1 = cat.add("x >= 1", lambda x: x >= 1)
# Items between 1.1 and 1.2, as a subcategory of items over 1
over_1.add("1.2 > x >= 1.1", lambda x: 1.2 > x >= 1.1)
over_1.add("x > 1.2", lambda x: x >= 1.2)

result = cat.categorise_list([0.01, 0.6, 1.001, 1.05, 1.1, 1.2, 3])
summarised = result.summarise()
print(summarised)
```
This should show something along the lines of:
```json
{
    "categories": [
        {"category_name": "x < 0.5", "matches": 1},
        {
            "category_name": "x >= 1", "matches": 5,
            "categories": [
                {"category_name": "1.2 > x >= 1.1", "matches": 1},
                {"category_name": "x > 1.2", "matches": 2},
                {"unmatched_items": 2}
            ]
        },
        {"unmatched_items": 1}
    ]
}
```

It is possible to obtain a Sankey diagram with plotly for the same
example.

First, install plotly
```shell
pip install plotly
```
Then:
```python
parameters = result.plotly_sankey(top_label="Top")

import plotly.graph_objects as go
fig = go.Figure(data=[go.Sankey(parameters)])
fig.update_layout(title_text="Example Sankey Diagram", font_size=20)
fig.show()
```

"""


setuptools.setup(
    name='simple-categorisation',
    version='0.2',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
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

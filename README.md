# Table of Contents <span class="tag" tag-name="TOC"><span class="smallcaps">TOC</span></span>

-   [Installation](#installation)
    -   [From pip](#from-pip)
    -   [From source](#from-source)
-   [Usages](#usages)
    -   [Named Entity Recognition](#named-entity-recognition)
-   [Contribution](#contribution)
    -   [Formatting Code](#formatting-code)

# Installation

## From pip

``` bash
pip install streamlit-gallery
```

## From source

``` bash
pip install git+https://github.com/Yevgnen/streamlit-gallery.git
```

# Usages

## Named Entity Recognition

``` Python
# -*- coding: utf-8 -*-

import streamlit_gallery

example = {
    "text": "But Google is starting from behind.",
    "ents": [{"start": 4, "end": 10, "label": "ORG"}],
}

streamlit_gallery.visualize_ner(example)
```

# Contribution

## Formatting Code

To ensure the codebase complies with a style guide, please use [flake8](https://github.com/PyCQA/flake8), [black](https://github.com/psf/black) and [isort](https://github.com/PyCQA/isort) tools to format and check codebase for compliance with PEP8.

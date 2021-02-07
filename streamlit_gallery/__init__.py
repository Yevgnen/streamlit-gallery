# -*- coding: utf-8 -*-

import collections
import random
from typing import Dict, Iterable, Mapping, Optional, Union

import spacy
import streamlit as st
from spacy import displacy
from streamlit_gallery.palette import Colors
from streamlit_gallery.utils import get_html, seed


def get_colors(k):
    if k <= 12:
        return Colors.PRESET12

    with seed(10000):
        return random.sample(Colors.PRESETS30, k)


def visualize_ner(
    example: Union[spacy.tokens.Doc, Dict],
    title: Optional[str] = None,
    colors: Optional[Union[Iterable[str], Mapping[str, str]]] = None,
):
    # Modified from: https://github.com/explosion/spacy-streamlit

    if isinstance(example, spacy.tokens.Doc):
        example = displacy.parse_ents(example)

    if any(
        prev["start"] >= cur["start"]
        for prev, cur in zip(example["ents"], example["ents"][1:])
    ):
        raise ValueError("Entities should be sorted in ascending order")

    labels = list({x["label"] for x in example["ents"]})

    if not colors:
        colors = get_colors(len(labels))

    if not isinstance(colors, collections.abc.Mapping):
        colors = dict(zip(labels, colors))

    if title:
        st.header(title)

    expander = st.sidebar.beta_expander("Select entity labels")
    selected_labels = expander.multiselect(
        "Entity labels", options=labels, default=labels
    )

    style = "<style>mark.entity { display: inline-block }</style>"
    kwargs = {
        "manual": True,
        "style": "ent",
        "options": {
            "ents": selected_labels,
            "colors": colors,
        },
    }
    html = displacy.render(example, **kwargs)
    html = get_html(html)

    st.write(style + html, unsafe_allow_html=True)


__all__ = [
    "visualize_ner",
]

__version__ = "0.1.0"

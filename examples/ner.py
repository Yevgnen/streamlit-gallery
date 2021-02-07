# -*- coding: utf-8 -*-

import streamlit_gallery

example = {
    "text": "But Google is starting from behind.",
    "ents": [{"start": 4, "end": 10, "label": "ORG"}],
}

streamlit_gallery.visualize_ner(example)

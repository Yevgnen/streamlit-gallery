# -*- coding: utf-8 -*-

import contextlib
import random


@contextlib.contextmanager
def seed(random_seed: int):
    state = random.getstate()
    random.seed(random_seed)
    yield
    random.setstate(state)


# References:
# https://github.com/explosion/spacy-streamlit/blob/1469c40dc88e04f681fea056ffeddaf2fbfb4382/spacy_streamlit/util.py#L26


def get_html(html: str) -> str:
    """Convert HTML so it can be rendered."""
    WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""
    # Newlines seem to mess with the rendering
    html = html.replace("\n", " ")

    return WRAPPER.format(html)

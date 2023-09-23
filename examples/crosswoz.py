# -*- coding: utf-8 -*-

import streamlit as st

from streamlit_crosswoz import CrossWOZDataset, CrossWOZVisualizer


def main():
    st.set_page_config(layout="wide")

    data_dir = "/Users/Maximin/datasets/nlp/CrossWOZ/data/crosswoz/"
    crosswoz = CrossWOZDataset(data_dir)

    visualizer = CrossWOZVisualizer(crosswoz)
    visualizer.visualize()


if __name__ == "__main__":
    main()

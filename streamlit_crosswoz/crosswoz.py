# -*- coding: utf-8 -*-

import json
import os
from typing import Dict, List, Mapping, Union

import pandas as pd
import streamlit as st


class CrossWOZDataset(object):
    def __init__(self, data_dir: str) -> None:
        self.data_dir = data_dir
        self.datasets = {
            mode: self.read_dataset(mode) for mode in ["train", "val", "test"]
        }
        self.database = {
            key: self.read_database(key)
            for key in ["attraction", "hotel", "metro", "restaurant", "taxi"]
        }

    @st.cache(allow_output_mutation=True)
    def _read_json(self, filename):  # pylint: disable=no-self-use
        with open(filename, mode="r", encoding="utf-8") as f:
            return json.load(f)

    def read_dataset(self, mode: str) -> Dict:
        return self._read_json(os.path.join(self.data_dir, f"{mode}.json"))

    def read_database(self, key: str) -> List:
        return self._read_json(os.path.join(self.data_dir, f"database/{key}_db.json"))

    def __getitem__(self, mode: str) -> Dict:
        return self.datasets[mode]


class CrossWOZVisualizer(object):
    # pylint: disable=no-self-use
    def __init__(self, dataset: CrossWOZDataset) -> None:
        self.dataset = dataset

    def _make_state_frame(self, obj):
        df = pd.DataFrame(obj, columns=["Id", "Domain", "Slot", "Value", "Selected"])
        df["Value"] = df["Value"].astype(str)

        return df

    def visualize_user_state(
        self, usr: Mapping, last_usr: Union[Mapping, None]
    ) -> None:
        def _style(df):
            df_style = pd.DataFrame("", index=df.index, columns=df.columns)
            if last_usr is None:
                return df_style

            df_last_state = self._make_state_frame(last_usr["user_state"])

            columns = ["Domain", "Slot", "Value", "Selected"]
            mask = df.loc[:, columns] != df_last_state.loc[:, columns]
            df_style[mask] = "color: #fa323c"

            return df_style

        st.subheader("User State")

        df_state = self._make_state_frame(usr["user_state"])
        st.table(df_state.style.apply(_style, axis=None))

    def visualize_system_state(
        self, sys: Mapping, last_sys: Union[Mapping, None]
    ) -> None:
        st.subheader("System State")

        columns = st.columns(len(sys["sys_state"]))
        for j, (key, value) in enumerate(sorted(sys["sys_state"].items())):
            state = pd.Series(value, dtype=str, name=key).to_frame()
            if last_sys:
                last_state = pd.Series(
                    last_sys["sys_state"][key], dtype=str, name=key
                ).to_frame()
                state = state.style.apply(
                    lambda df: (df != last_state).applymap(
                        lambda x: "color: #fa323c" if x else ""
                    ),
                    axis=None,
                )

            columns[j].dataframe(state)

    def visualize_dialog_act(self, usr: Mapping, sys: Mapping) -> None:
        st.subheader("Dialog Act")

        columns = st.columns(2)
        for i, (obj, name) in enumerate(zip([usr, sys], ["User", "System"])):
            columns[i].subheader(name)
            df_dialog_act = pd.DataFrame(
                obj["dialog_act"],
                columns=["Intent", "Domain", "Slot", "Value"],
            )
            df_dialog_act["Value"] = df_dialog_act["Value"].astype(str)
            columns[i].table(df_dialog_act)

    def visualize_task(self, example: Mapping) -> None:
        st.header(f"Task Description ({example['type']})")

        for i, desc in enumerate(example["task description"]):
            st.markdown(f"{i + 1}. {desc}")

    def visualize_goal(self, example: Mapping) -> None:
        st.header("Goal")

        df_goal = self._make_state_frame(example["goal"])
        df_goal.insert(4, "Final Value", [str(x[-2]) for x in example["final_goal"]])
        st.table(df_goal)

    def visualize_turn(
        self,
        i: int,
        usr: Mapping,
        sys: Mapping,
        last_usr: Union[Mapping, None],
        last_sys: Union[Mapping, None],
    ) -> None:
        st.header(f"Turn #{i}")

        st.markdown(f'- {usr["role"]}: {usr["content"]}')
        st.markdown(f'- {sys["role"]}: {sys["content"]}')

        self.visualize_user_state(usr, last_usr)
        self.visualize_system_state(sys, last_sys)
        self.visualize_dialog_act(usr, sys)

    def visualize_database(self, filename: str) -> None:
        st.header(filename)

        key = os.path.splitext(os.path.basename(filename))[0].split("_")[0]
        st.table(pd.DataFrame([x[1] for x in self.dataset.database[key]]))

    def visualize_dataset(self, filename: str) -> None:
        mode = filename.split(".")[0]
        dataset = self.dataset[mode]

        all_types = {x["type"] for x in dataset.values()}
        types = set(st.sidebar.multiselect("Select types", all_types, all_types))

        example_ids = [key for key, value in dataset.items() if value["type"] in types]
        example_id = st.sidebar.selectbox(
            f"Select example ({len(example_ids)} total)", example_ids
        )
        example = dataset[example_id]

        self.visualize_task(example)
        self.visualize_goal(example)

        def iter_turns():
            for i in range(0, len(example["messages"]), 2):
                yield example["messages"][i : i + 2]

        last_usr, last_sys = None, None
        for i, (usr, sys) in enumerate(iter_turns()):
            self.visualize_turn(i, usr, sys, last_usr, last_sys)
            last_usr, last_sys = usr, sys

    def visualize(self) -> None:
        st.sidebar.title("CrossWOZ Dataset Viewer")

        factory = {
            "train.json": self.visualize_dataset,
            "val.json": self.visualize_dataset,
            "test.json": self.visualize_dataset,
            "database/attraction_db.json": self.visualize_database,
            "database/hotel_db.json": self.visualize_database,
            "database/metro_db.json": self.visualize_database,
            "database/restaurant_db.json": self.visualize_database,
            "database/taxi_db.json": self.visualize_database,
        }

        filename = st.sidebar.selectbox("Select file", factory)
        factory[filename](filename)

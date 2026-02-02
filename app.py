# app.py (snippet)

from schemes import SCHEMES
from logic import evaluate_scheme
import streamlit as st

scheme = SCHEMES["Startup India"]

st.subheader("Startup India – Eligibility Check")

for attr, meta in scheme["required_attributes"].items():
    if attr not in st.session_state.user:

        st.caption(f"Why we ask: {meta['why']}")

        if meta["type"] == "boolean":
            st.session_state.user[attr] = st.radio(
                meta["question"], [True, False]
            )

        elif meta["type"] == "number":
            st.session_state.user[attr] = st.number_input(
                meta["question"], min_value=0
            )

        elif meta["type"] == "select":
            st.session_state.user[attr] = st.selectbox(
                meta["question"], meta["options"]
            )

        elif meta["type"] == "text":
            st.session_state.user[attr] = st.text_input(
                meta["question"]
            )

        st.rerun()


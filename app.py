import streamlit as st
from schemes import SCHEMES
from logic import evaluate_scheme

# ---- Session Init ----
if "user" not in st.session_state:
    st.session_state.user = {}

scheme = SCHEMES["Startup India"]

st.title("Startup India – Eligibility Check")

# ---- Ask ONE question at a time ----
for attr, meta in scheme["required_attributes"].items():

    if attr not in st.session_state.user:

        st.caption(f"Why we ask: {meta['why']}")

        answer = None

        if meta["type"] == "boolean":
            answer = st.radio(meta["question"], ["Yes", "No"])

        elif meta["type"] == "number":
            answer = st.number_input(meta["question"], min_value=0)

        elif meta["type"] == "select":
            answer = st.selectbox(meta["question"], meta["options"])

        elif meta["type"] == "text":
            answer = st.text_input(meta["question"])

        # 👇 EXPLICIT SUBMIT
        if st.button("Next"):
            if meta["type"] == "boolean":
                answer = True if answer == "Yes" else False

            st.session_state.user[attr] = answer
            st.rerun()

        # 🚨 STOP further rendering
        st.stop()

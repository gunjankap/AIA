import streamlit as st
from schemes import SCHEMES
from logic import evaluate_scheme

st.set_page_config(page_title="Startup Scheme Advisor", layout="centered")

st.title("🚀 AI Startup & MSME Scheme Advisor")

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.user = {}

# STEP 0: Persona
if st.session_state.step == 0:
    persona = st.radio(
        "Which best describes you?",
        ["Student Entrepreneur", "Early/Budding Entrepreneur", "MSME / Business Owner"]
    )

    if st.button("Continue"):
        st.session_state.user["persona"] = (
            "student" if persona.startswith("Student")
            else "early" if persona.startswith("Early")
            else "msme"
        )
        st.session_state.step = 1
        st.experimental_rerun()

# STEP 1: Common Questions
elif st.session_state.step == 1:
    st.subheader("Tell us about your startup")

    st.session_state.user["registered"] = st.radio(
        "Is your business registered?", [True, False]
    )

    st.session_state.user["startup_stage"] = st.selectbox(
        "Startup stage", ["Idea", "Prototype", "Pilot", "Revenue-generating"]
    )

    st.session_state.user["turnover"] = st.selectbox(
        "Annual Turnover (₹ in Lakhs)",
        [0, 5, 20, 50, 100]
    )

    if st.button("Evaluate Schemes"):
        st.session_state.step = 2
        st.experimental_rerun()

# STEP 2: Results
elif st.session_state.step == 2:
    st.subheader("📋 Scheme Eligibility Results")

    for name, scheme in SCHEMES.items():
        if st.session_state.user["persona"] not in scheme["personas"]:
            continue

        status, reasons = evaluate_scheme(scheme, st.session_state.user)

        with st.expander(f"{name} — {status}"):
            if reasons:
                for r in reasons:
                    st.write("•", r)
            else:
                st.success("You meet all eligibility criteria")

            st.write("📄 Documents Required:")
            for d in scheme["documents"]:
                st.write("-", d)

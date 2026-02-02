import streamlit as st
from schemes import SCHEMES
from logic import evaluate_scheme

# ---------------- SESSION INIT ----------------
if "page" not in st.session_state:
    st.session_state.page = "persona"

if "user" not in st.session_state:
    st.session_state.user = {}

if "result" not in st.session_state:
    st.session_state.result = {}

# ---------------- NAV HELPER ----------------
def go(page):
    st.session_state.page = page
    st.rerun()

# ---------------- PAGE 1: PERSONA ----------------
def persona_page():
    st.title("Entrepreneur Persona")

    persona = st.radio(
        "Which best describes you?",
        [
            "🎓 Student Entrepreneur",
            "🌱 Early Entrepreneur",
            "🏭 MSME / Business Owner"
        ]
    )

    if st.button("Next"):
        if "Student" in persona:
            st.session_state.user = {"persona": "student"}
        elif "Early" in persona:
            st.session_state.user = {"persona": "early"}
        else:
            st.session_state.user = {"persona": "msme"}

        go("form")

# ---------------- PAGE 2: SINGLE-PAGE FORM ----------------
def form_page():
    st.title("Eligibility Assessment")
    st.button("⬅ Back", on_click=lambda: go("persona"))

    persona = st.session_state.user["persona"]

    # Select applicable schemes
    schemes = {
        k: v for k, v in SCHEMES.items()
        if persona in v["personas"]
    }

    scheme_name = list(schemes.keys())[0]
    scheme = schemes[scheme_name]

    st.subheader(scheme_name)
    st.caption("Answer the following questions to assess eligibility")

    with st.form("eligibility_form"):
        responses = {}

        for attr, meta in scheme["required_attributes"].items():
            st.markdown(f"**{meta['question']}**")
            st.caption(f"Why we ask: {meta['why']}")

            if meta["type"] == "boolean":
                responses[attr] = st.radio(
                    "", ["Yes", "No"], key=attr
                )

            elif meta["type"] == "number":
                responses[attr] = st.number_input(
                    "", min_value=0, key=attr
                )

            elif meta["type"] == "select":
                responses[attr] = st.selectbox(
                    "", meta["options"], key=attr
                )

            elif meta["type"] == "text":
                responses[attr] = st.text_input(
                    "", key=attr
                )

            st.divider()

        submitted = st.form_submit_button("Evaluate Eligibility")

    if submitted:
        for attr, val in responses.items():
            if val in ["Yes", "No"]:
                st.session_state.user[attr] = True if val == "Yes" else False
            else:
                st.session_state.user[attr] = val

        st.session_state.user["scheme"] = scheme_name
        go("engine")

# ---------------- PAGE 3: RULE ENGINE ----------------
def engine_page():
    st.title("Rule-Based Eligibility Engine")
    st.button("⬅ Back", on_click=lambda: go("form"))

    scheme = SCHEMES[st.session_state.user["scheme"]]
    status, reasons = evaluate_scheme(scheme, st.session_state.user)

    st.session_state.result = {
        "status": status,
        "reasons": reasons,
        "scheme": scheme
    }

    st.success(f"Eligibility Status: {status}")

    if st.button("Explain Decision"):
        go("explain")

# ---------------- PAGE 4: EXPLANATION ----------------
def explain_page():
    st.title("AI Explanation Layer")
    st.button("⬅ Back", on_click=lambda: go("engine"))

    res = st.session_state.result

    st.write(f"**Status:** {res['status']}")

    if res["reasons"]:
        st.write("### Reasons")
        for r in res["reasons"]:
            st.write("-", r)
    else:
        st.write("You satisfy all eligibility conditions.")

    if st.button("View Advisory Report"):
        go("report")

# ---------------- PAGE 5: REPORT ----------------
def report_page():
    st.title("Scheme Advisory Report")
    st.button("⬅ Back", on_click=lambda: go("explain"))

    scheme = st.session_state.result["scheme"]

    st.write("### Recommended Scheme")
    st.write("**Purpose:**", scheme["purpose"])
    st.write("**Source:**", scheme["source"])

    st.success("Next steps: documentation & application guidance")

# ---------------- ROUTER ----------------
if st.session_state.page == "persona":
    persona_page()
elif st.session_state.page == "form":
    form_page()
elif st.session_state.page == "engine":
    engine_page()
elif st.session_state.page == "explain":
    explain_page()
elif st.session_state.page == "report":
    report_page()

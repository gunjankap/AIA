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

# ---------------- PAGE 1 ----------------
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
            st.session_state.user["persona"] = "student"
        elif "Early" in persona:
            st.session_state.user["persona"] = "early"
        else:
            st.session_state.user["persona"] = "msme"

        go("chat")

# ---------------- PAGE 2 ----------------
def chat_page():
    st.title("Adaptive Eligibility Chat")
    st.button("⬅ Back", on_click=lambda: go("persona"))

    persona = st.session_state.user["persona"]

    schemes = {
        k: v for k, v in SCHEMES.items()
        if persona in v["personas"]
    }

    scheme_name = list(schemes.keys())[0]
    scheme = schemes[scheme_name]

    st.subheader(scheme_name)

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
            else:
                answer = st.text_input(meta["question"])

            if st.button("Next"):
                if meta["type"] == "boolean":
                    answer = True if answer == "Yes" else False

                st.session_state.user[attr] = answer
                st.rerun()

            st.stop()

    st.session_state.user["scheme"] = scheme_name
    go("engine")

# ---------------- PAGE 3 ----------------
def engine_page():
    st.title("Rule-Based Eligibility Engine")
    st.button("⬅ Back", on_click=lambda: go("chat"))

    scheme = SCHEMES[st.session_state.user["scheme"]]

    status, reasons = evaluate_scheme(scheme, st.session_state.user)

    st.session_state.result = {
        "status": status,
        "reasons": reasons,
        "scheme": scheme
    }

    st.success(f"Status: {status}")

    if st.button("Explain Decision"):
        go("explain")

# ---------------- PAGE 4 ----------------
def explain_page():
    st.title("AI Explanation Layer")
    st.button("⬅ Back", on_click=lambda: go("engine"))

    res = st.session_state.result

    st.write(f"**Eligibility Status:** {res['status']}")

    if res["reasons"]:
        st.write("### Reasons")
        for r in res["reasons"]:
            st.write("-", r)
    else:
        st.write("You satisfy all eligibility conditions.")

    if st.button("View Advisory Report"):
        go("report")

# ---------------- PAGE 5 ----------------
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
elif st.session_state.page == "chat":
    chat_page()
elif st.session_state.page == "engine":
    engine_page()
elif st.session_state.page == "explain":
    explain_page()
elif st.session_state.page == "report":
    report_page()

import streamlit as st
import pandas as pd

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Agentic AI Career Growth Agent",
    layout="wide"
)

# ============================================================
# LOAD DATASETS
# ============================================================
@st.cache_data
def load_data():
    employee_df = pd.read_csv("employee_data.csv")
    jobs_df = pd.read_csv("job_openings.csv")
    return employee_df, jobs_df

employee_df, jobs_df = load_data()

# ============================================================
# TITLE SECTION
# ============================================================
st.title("🚀 Agentic AI Career Growth Automation System")
st.subheader("MBA Project Demo: Autonomous Upskilling + Internal Mobility Agent")

st.markdown("""
This prototype demonstrates an **Agentic AI Career Coach** that:
- Diagnoses employee skill gaps  
- Creates personalized learning journeys  
- Triggers reminders and review scheduling  
- Suggests future internal job roles  

✅ Designed as the future of AI-powered Talent Management.
""")

st.divider()

# ============================================================
# SIDEBAR: EMPLOYEE SELECTION
# ============================================================
st.sidebar.header("👤 Select Employee")

employee_name = st.sidebar.selectbox(
    "Choose an employee profile:",
    employee_df["Name"].tolist()
)

selected_employee = employee_df[employee_df["Name"] == employee_name].iloc[0]

st.sidebar.divider()
run_agent = st.sidebar.button("⚡ Run Career Growth Agent")

# ============================================================
# MAIN OUTPUT
# ============================================================
if run_agent:

    st.success(f"✅ Career Growth Agent Activated for {employee_name}")

    # Extract employee details
    role = selected_employee["Current_Role"]
    dept = selected_employee["Department"]
    skills = selected_employee["Current_Skills"]
    goal = selected_employee["Career_Goal"]
    rating = selected_employee["Performance_Rating"]
    next_role = selected_employee["Recommended_Next_Role"]

    # ============================================================
    # SECTION 1: EMPLOYEE SUMMARY
    # ============================================================
    st.header("📌 Employee Career Profile")

    col1, col2 = st.columns(2)

    with col1:
        st.info("Employee Overview")
        st.write("**Role:**", role)
        st.write("**Department:**", dept)
        st.write("**Current Skills:**", skills)

    with col2:
        st.info("Career Intent")
        st.write("**Career Goal:**", goal)
        st.write("**Performance Rating:**", rating, "/5")
        st.write("**Recommended Next Role:**", next_role)

    st.divider()

    # ============================================================
    # SECTION 2: SKILL GAP DIAGNOSIS (AUTOMATED)
    # ============================================================
    st.header("🧠 Agent Task 1: Skill Gap Diagnosis")

    st.markdown("### Missing Skills Identified (Agent Output):")

    missing_skills = [
        "Python for Analytics",
        "Machine Learning Fundamentals",
        "Generative AI Applications",
        "Agentic Workflow Automation Tools"
    ]

    for skill in missing_skills:
        st.write("✅", skill)

    st.divider()

    # ============================================================
    # SECTION 3: LEARNING JOURNEY GENERATION
    # ============================================================
    st.header("📚 Agent Task 2: Personalized Learning Roadmap")

    st.markdown("### 6-Week Career Upskilling Plan")

    roadmap = {
        "Week 1–2": "Python Basics + Data Handling",
        "Week 3": "Machine Learning Intro",
        "Week 4": "Generative AI for Business Use Cases",
        "Week 5": "Mini Capstone Project",
        "Week 6": "Certification + Role Readiness Review"
    }

    for week, task in roadmap.items():
        st.write(f"**{week}:** {task}")

    st.divider()

    # ============================================================
    # SECTION 4: AGENTIC AUTOMATION ACTIONS
    # ============================================================
    st.header("🤖 Agent Task 3: Automation Actions")

    col3, col4, col5 = st.columns(3)

    # Reminder Automation
    with col3:
        st.subheader("🔔 Reminder Trigger")
        st.write("Agent monitors learning progress weekly.")
        if st.button("Send Reminder"):
            st.warning("📩 Reminder Sent: Complete Week 2 Python module!")

    # Review Scheduling Automation
    with col4:
        st.subheader("📅 Progress Review Scheduling")
        st.write("Agent schedules quarterly career check-ins.")
        if st.button("Schedule Review Meeting"):
            st.success("✅ Career Review Meeting Scheduled with Manager!")

    # Role Match Automation
    with col5:
        st.subheader("💼 Internal Role Matching")
        st.write("Agent finds best future internal roles.")
        if st.button("Check Job Matches"):
            st.info(f"⭐ Suggested Role Match: {next_role} (80% readiness)")

    st.divider()

    # ============================================================
    # SECTION 5: INTERNAL JOB OPENINGS MATCHING
    # ============================================================
    st.header("🏢 Agent Task 4: Internal Opportunity Scan")

    st.markdown("### Available Job Openings in Organization")

    st.dataframe(jobs_df)

    st.divider()

    # ============================================================
    # FINAL SUMMARY REPORT
    # ============================================================
    st.header("📊 Agentic Career Growth Summary Report")

    st.markdown(f"""
    ✅ **Employee:** {employee_name}  
    ✅ **Current Role:** {role}  
    ✅ **Career Goal:** {goal}  
    ✅ **Skill Readiness Level:** 70%  
    ✅ **Next Recommended Role:** {next_role}  
    ✅ **Next Action:** Complete Python + ML Upskilling Journey  
    """)

    st.success("🚀 Agent Completed First Autonomous Career Development Cycle!")

# ============================================================
# END OF APP
# ============================================================

import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Chikki's Study Career Planner",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

TASK_FILE = "study_tasks.csv"
SKILL_FILE = "skills.csv"

# -------------------- LOAD TASKS --------------------

task_columns = ["Subject", "Study Time", "Date", "Priority", "Completed"]

if os.path.exists(TASK_FILE):
    try:
        study_tasks = pd.read_csv(TASK_FILE)
    except Exception:
        study_tasks = pd.DataFrame(columns=task_columns)
else:
    study_tasks = pd.DataFrame(columns=task_columns)

for col in task_columns:
    if col not in study_tasks.columns:
        study_tasks[col] = False if col == "Completed" else ""

study_tasks = study_tasks[task_columns].copy()
study_tasks["Study Time"] = pd.to_numeric(
    study_tasks["Study Time"], errors="coerce"
).fillna(0)
study_tasks["Completed"] = (
    study_tasks["Completed"].astype(str).str.lower()
    .isin(["true", "1", "yes"])
)

# -------------------- LOAD SKILLS --------------------

if os.path.exists(SKILL_FILE):
    try:
        skills = pd.read_csv(SKILL_FILE)
    except Exception:
        skills = pd.DataFrame(columns=["Skill", "Level"])
else:
    skills = pd.DataFrame(columns=["Skill", "Level"])

for col in ["Skill", "Level"]:
    if col not in skills.columns:
        skills[col] = ""

skills = skills[["Skill", "Level"]].copy()

# -------------------- FINAL COLOR THEME --------------------

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 10% 5%, rgba(45,212,191,.18), transparent 27%),
        radial-gradient(circle at 90% 10%, rgba(139,92,246,.20), transparent 28%),
        linear-gradient(135deg, #07141c 0%, #0b1f2d 48%, #171633 100%);
    color: #f7fbff;
}

header[data-testid="stHeader"] {
    background: rgba(7,20,28,.92) !important;
}

h1, h2, h3 {
    color: #f8fbff !important;
    font-weight: 800 !important;
}

h1 {
    font-size: 42px !important;
}

p, label, span {
    color: #dcecf5;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071820, #102b3c, #211b43);
    border-right: 1px solid rgba(45,212,191,.25);
}

section[data-testid="stSidebar"] * {
    color: #f4fbff !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: rgba(45,212,191,.08);
    border: 1px solid rgba(45,212,191,.16);
    border-radius: 14px;
    padding: 11px 13px;
    margin-bottom: 8px;
    transition: .2s;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: linear-gradient(90deg, #168f91, #6748c7);
    transform: translateX(4px);
}

div[data-testid="metric-container"] {
    background: linear-gradient(145deg, rgba(17,50,67,.96), rgba(37,35,76,.96));
    border: 1px solid rgba(86,211,205,.28);
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 12px 30px rgba(0,0,0,.28);
}

div[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 30px !important;
    font-weight: 800 !important;
}

.stButton > button {
    width: 100%;
    border: 0;
    border-radius: 13px;
    padding: 11px 18px;
    background: linear-gradient(90deg, #159a9c, #6750d9);
    color: white !important;
    font-weight: 750;
    box-shadow: 0 8px 20px rgba(21,154,156,.20);
    transition: .2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    background: linear-gradient(90deg, #20b9b3, #7c63eb);
}

.stTextInput input,
.stNumberInput input,
.stDateInput input {
    background: #0b1c2a !important;
    color: #ffffff !important;
    border: 1px solid #315267 !important;
    border-radius: 12px !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: #0b1c2a !important;
    color: white !important;
    border-radius: 12px !important;
}

div[data-testid="stAlert"] {
    border-radius: 14px;
}

hr {
    border-color: rgba(86,211,205,.22);
}

</style>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------

st.sidebar.markdown("## 🎓 Chikki's Study Space")
st.sidebar.caption("Plan • Learn • Track • Grow")
st.sidebar.divider()

page = st.sidebar.radio(
    "MENU",
    [
        "🏠 Dashboard",
        "📚 Study Planner",
        "🎯 Career Planner",
        "💡 Skills Tracker",
        "📊 Analytics",
        "ℹ️ About My Project"
    ]
)

# -------------------- DASHBOARD --------------------

if page == "🏠 Dashboard":

    st.title("🎓 Chikki's Study Career Planner")

    st.markdown("""
    <div style="
        padding:20px;
        border-radius:18px;
        background:linear-gradient(
            135deg,
            rgba(21,154,156,.25),
            rgba(103,80,217,.30)
        );
        border:1px solid rgba(86,211,205,.25);
        margin-bottom:22px;
    ">
        <h3 style="margin:0;color:white;">
            👋 Welcome to My Study Space
        </h3>
        <p style="margin:8px 0 0;color:#dcecf5;">
            I created this app to manage my studies, track the
            skills I am learning, and plan my career journey
            in one place. 🚀
        </p>
    </div>
    """, unsafe_allow_html=True)

    total_tasks = len(study_tasks)
    completed = int(study_tasks["Completed"].sum()) if total_tasks else 0
    total_hours = float(study_tasks["Study Time"].sum()) if total_tasks else 0
    progress = completed / total_tasks * 100 if total_tasks else 0

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("📚 Total Tasks", total_tasks)
    with c2:
        st.metric("⏱️ Study Hours", f"{total_hours:.1f}")
    with c3:
        st.metric("✅ Completed", completed)
    with c4:
        st.metric("📈 Progress", f"{progress:.0f}%")

    st.divider()
    st.subheader("🌱 My Learning Journey")

    if total_tasks == 0:
        st.info("No study tasks yet. Start from 📚 Study Planner.")
    else:
        st.success(
            f"Great! You currently have {total_tasks} task(s). Keep moving forward. 💪"
        )

        st.subheader("📝 Recent Tasks")
        recent = study_tasks.tail(5).copy()
        recent["Status"] = recent["Completed"].map(
            {True: "✅ Done", False: "⏳ Pending"}
        )

        st.dataframe(
            recent[["Subject", "Study Time", "Date", "Priority", "Status"]],
            use_container_width=True,
            hide_index=True
        )

# -------------------- STUDY PLANNER --------------------

elif page == "📚 Study Planner":

    st.header("📚 My Study Planner")
    st.write("Plan my daily study tasks and stay consistent.")
    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        subject = st.text_input(
            "📖 Subject",
            placeholder="e.g. Python, SQL, Mathematics"
        )
        study_time = st.number_input(
            "⏱️ Study Time (hours)",
            min_value=0.5,
            max_value=12.0,
            value=1.0,
            step=0.5
        )

    with c2:
        study_date = st.date_input("📅 Study Date")
        priority = st.selectbox(
            "⭐ Priority",
            ["High", "Medium", "Low"]
        )

    if st.button("➕ Add Study Task", key="add_task"):
        if not subject.strip():
            st.warning("Please enter a subject first.")
        else:
            new_task = pd.DataFrame([{
                "Subject": subject.strip(),
                "Study Time": study_time,
                "Date": str(study_date),
                "Priority": priority,
                "Completed": False
            }])

            study_tasks = pd.concat(
                [study_tasks, new_task], ignore_index=True
            )
            study_tasks.to_csv(TASK_FILE, index=False)

            st.success("Study task added successfully! 🎉")
            st.rerun()

    st.divider()
    st.subheader("📋 My Study Tasks")

    if study_tasks.empty:
        st.info("No tasks yet. Add your first task above.")
    else:

        for i in range(len(study_tasks)):
            task = study_tasks.iloc[i]

            c1, c2, c3, c4 = st.columns([3, 1.4, 1.4, 1.5])

            with c1:
                st.write(f"**📖 {task['Subject']}**")
                st.caption(str(task["Date"]))

            with c2:
                st.write(f"⏱️ {task['Study Time']} hrs")

            with c3:
                st.write(f"⭐ {task['Priority']}")

            with c4:
                current = bool(task["Completed"])
                checked = st.checkbox(
                    "Completed",
                    value=current,
                    key=f"completed_{i}"
                )

                if checked != current:
                    study_tasks.loc[
                        study_tasks.index[i], "Completed"
                    ] = checked
                    study_tasks.to_csv(TASK_FILE, index=False)
                    st.rerun()

        st.divider()
        st.subheader("🗑️ Delete a Task")

        delete_index = st.selectbox(
            "Select task to delete",
            range(len(study_tasks)),
            format_func=lambda x:
                f"{x + 1}. {study_tasks.iloc[x]['Subject']}",
            key="delete_select"
        )

        if st.button("🗑️ Delete Selected Task", key="delete_button"):
            study_tasks = study_tasks.drop(
                study_tasks.index[delete_index]
            ).reset_index(drop=True)
            study_tasks.to_csv(TASK_FILE, index=False)
            st.success("Task deleted successfully! ✅")
            st.rerun()

        st.divider()
        st.subheader("✏️ Edit a Task")

        edit_index = st.selectbox(
            "Select task to edit",
            range(len(study_tasks)),
            format_func=lambda x:
                f"{x + 1}. {study_tasks.iloc[x]['Subject']}",
            key="edit_select"
        )

        selected = study_tasks.iloc[edit_index]

        new_subject = st.text_input(
            "📖 Subject",
            value=str(selected["Subject"]),
            key="edit_subject"
        )

        new_time = st.number_input(
            "⏱️ Study Time (hours)",
            min_value=0.5,
            max_value=12.0,
            value=float(selected["Study Time"]),
            step=0.5,
            key="edit_time"
        )

        new_priority = st.selectbox(
            "⭐ Priority",
            ["High", "Medium", "Low"],
            index=["High", "Medium", "Low"].index(
                str(selected["Priority"])
            ),
            key="edit_priority"
        )

        if st.button("💾 Save Changes", key="save_changes"):
            study_tasks.loc[
                study_tasks.index[edit_index], "Subject"
            ] = new_subject.strip()

            study_tasks.loc[
                study_tasks.index[edit_index], "Study Time"
            ] = new_time

            study_tasks.loc[
                study_tasks.index[edit_index], "Priority"
            ] = new_priority

            study_tasks.to_csv(TASK_FILE, index=False)
            st.success("Task updated successfully! 🎉")
            st.rerun()

# -------------------- CAREER PLANNER --------------------

elif page == "🎯 Career Planner":

    st.header("🎯 My Career Planner")
    st.write("Create a roadmap for the career I want to build.")
    st.divider()

    career = st.selectbox(
        "💼 Choose my career goal",
        [
            "Data Analyst",
            "Data Scientist",
            "AI / ML Engineer",
            "Software Developer",
            "Web Developer",
            "Other"
        ]
    )

    target = st.text_input(
        "🎯 My career target",
        placeholder="e.g. Get a Data Analyst internship"
    )

    if st.button("🚀 Create My Career Roadmap", key="career_button"):

        roadmaps = {
            "Data Analyst": [
                "Learn Excel",
                "Learn SQL",
                "Learn Python",
                "Learn Power BI / Tableau",
                "Build data analysis projects",
                "Create a portfolio",
                "Apply for internships/jobs"
            ],
            "Data Scientist": [
                "Learn Python",
                "Learn Statistics",
                "Learn SQL",
                "Learn Machine Learning",
                "Learn Deep Learning",
                "Build projects",
                "Create a portfolio"
            ],
            "AI / ML Engineer": [
                "Learn Python",
                "Learn Mathematics",
                "Learn Machine Learning",
                "Learn Deep Learning",
                "Learn NLP / Computer Vision",
                "Build AI projects",
                "Deploy projects"
            ],
            "Software Developer": [
                "Learn Programming",
                "Learn Data Structures",
                "Learn Git & GitHub",
                "Build projects",
                "Practice coding",
                "Create a portfolio",
                "Apply for opportunities"
            ],
            "Web Developer": [
                "Learn HTML",
                "Learn CSS",
                "Learn JavaScript",
                "Learn a frontend framework",
                "Learn backend development",
                "Build websites",
                "Deploy projects"
            ],
            "Other": [
                "Research my target career",
                "Identify required skills",
                "Learn those skills",
                "Build relevant projects",
                "Create a portfolio",
                "Apply for opportunities"
            ]
        }

        st.success(f"My roadmap for {career} is ready! 🎉")

        if target.strip():
            st.info(f"🎯 My target: {target}")

        st.subheader("🛣️ My Career Roadmap")

        for number, step in enumerate(roadmaps[career], 1):
            st.write(f"**Step {number} —** {step}")

# -------------------- SKILLS TRACKER --------------------

elif page == "💡 Skills Tracker":

    st.header("💡 My Skills Tracker")
    st.write("Track the technical skills I am learning.")
    st.divider()

    skill = st.text_input(
        "🧠 Skill I am learning",
        placeholder="e.g. Python, SQL, Power BI"
    )

    level = st.select_slider(
        "📈 My current level",
        options=["Beginner", "Intermediate", "Advanced"]
    )

    if st.button("➕ Add My Skill", key="add_skill"):

        if not skill.strip():
            st.warning("Please enter a skill first.")
        else:
            new_skill = pd.DataFrame([{
                "Skill": skill.strip(),
                "Level": level
            }])

            skills = pd.concat(
                [skills, new_skill], ignore_index=True
            )
            skills.to_csv(SKILL_FILE, index=False)

            st.success(f"{skill} added to my skills! 🎉")
            st.rerun()

    st.divider()
    st.subheader("📊 My Skills")

    if skills.empty:
        st.info("No skills added yet. Start building your skill list.")
    else:

        for i, row in skills.iterrows():

            c1, c2, c3 = st.columns([3, 2, 1])

            with c1:
                st.write(f"**🧠 {row['Skill']}**")

            with c2:
                skill_progress = {
                    "Beginner": 0.33,
                    "Intermediate": 0.66,
                    "Advanced": 1.0
                }.get(str(row["Level"]), 0)

                st.progress(skill_progress)
                st.caption(str(row["Level"]))

            with c3:
                if st.button("🗑️", key=f"delete_skill_{i}"):
                    skills = skills.drop(
                        skills.index[i]
                    ).reset_index(drop=True)
                    skills.to_csv(SKILL_FILE, index=False)
                    st.rerun()

# -------------------- ANALYTICS --------------------

elif page == "📊 Analytics":

    st.header("📊 My Analytics")
    st.write("A simple overview of my study performance.")
    st.divider()

    total = len(study_tasks)

    if total:
        completed = int(study_tasks["Completed"].sum())
        pending = total - completed
        hours = float(study_tasks["Study Time"].sum())
        progress = completed / total

        high = int(
            (study_tasks["Priority"] == "High").sum()
        )
        medium = int(
            (study_tasks["Priority"] == "Medium").sum()
        )
        low = int(
            (study_tasks["Priority"] == "Low").sum()
        )
    else:
        completed = 0
        pending = 0
        hours = 0
        progress = 0
        high = 0
        medium = 0
        low = 0

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("📚 Total Tasks", total)

    with c2:
        st.metric("✅ Completed", completed)

    with c3:
        st.metric("⏳ Pending", pending)

    c4, c5 = st.columns(2)

    with c4:
        st.metric("⏱️ Total Study Hours", f"{hours:.1f}")

    with c5:
        st.metric("📈 Completion Rate", f"{progress * 100:.0f}%")

    st.divider()
    st.subheader("📈 My Overall Progress")
    st.progress(progress)
    st.write(f"**{completed} of {total} tasks completed.**")

    st.divider()
    st.subheader("⭐ Priority Breakdown")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("🔴 High Priority", high)

    with c2:
        st.metric("🟡 Medium Priority", medium)

    with c3:
        st.metric("🟢 Low Priority", low)

    st.divider()
    st.subheader("💡 My Study Insight")

    if total == 0:
        st.info("Start adding study tasks to see my analytics.")
    elif progress == 1:
        st.success("Amazing! 🎉 I completed all my tasks.")
    elif progress >= 0.5:
        st.success(
            "Great progress! I am more than halfway there. 💪"
        )
    else:
        st.info(
            "I will keep going. Small daily progress matters. 🌱"
        )

# -------------------- ABOUT --------------------

elif page == "ℹ️ About My Project":

    st.header("ℹ️ About My Project")

    st.markdown("""
### 🎓 Study Career Planner

This is my personal Python project designed to help me
organize my study routine and career preparation in one place.

### ✨ What I built

- 📚 Study task management
- ✅ Task completion tracking
- ✏️ Edit and 🗑️ delete functionality
- 🎯 Career roadmaps
- 💡 Skills tracking
- 📊 Study analytics
- 💾 Local data saving using CSV files

### 🛠️ Technologies Used

**Python • Streamlit • Pandas • CSV**

### 🌱 Why I made it

I wanted to create something practical that I could actually
use while learning Python and developing my technical skills.

### 🚀 My Goal

Keep improving this project as I learn more about Python,
data handling, UI design and application development.
""")

    st.divider()

    st.success(
        "Built as my personal learning project with Python & Streamlit. 💙"
    )

# -------------------- FOOTER --------------------

st.sidebar.divider()
st.sidebar.markdown("### ✨ My Learning Journey")
st.sidebar.caption("🎓 Study • 💡 Skills • 🎯 Career")
st.sidebar.caption("Built with Python & Streamlit")
st.sidebar.caption("Created by Chikki ❤️")

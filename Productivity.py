import streamlit as  st
import pandas as pd
import time
import os
import datetime


# --- Page Configuration ---
st.set_page_config(page_title="My AI Assistant", page_icon="🤖")

# --- Title and Header ---
st.title("🤖 Personal Productivity Assistant")
st.write("Welcome! Let's organize your life and boost your focus.")

# --- File for persistence ---
TASKS_FILE = "tasks.csv"

# --- Load tasks if file exists ---
if 'tasks' not in st.session_state:
    if os.path.exists(TASKS_FILE):
        st.session_state.tasks = pd.read_csv(TASKS_FILE).to_dict('records')
    else:
        st.session_state.tasks = []

# --- Sidebar for Inputs ---
st.sidebar.header("Add New Task")
task_name = st.sidebar.text_input("What do you need to do?")
priority = st.sidebar.select_slider("Priority Level", options=["Low", "Medium", "High", "Critical"])
time_est = st.sidebar.slider("Estimated Time (mins)", 15, 120, 30)

# --- Function to Add Task ---
if st.sidebar.button("Add Task"):
    if task_name:
        new_task = {"Task": task_name, "Priority": priority, "Time": time_est, "Status": "Pending"}
        st.session_state.tasks.append(new_task)
        pd.DataFrame(st.session_state.tasks).to_csv(TASKS_FILE, index=False)  # Save persistently
        st.sidebar.success("Task Added!")
    else:
        st.sidebar.warning("Please enter a task name.")

# --- MAIN DASHBOARD AREA ---
if len(st.session_state.tasks) > 0:
    df = pd.DataFrame(st.session_state.tasks)

    # Sorting & Filtering
    sort_by = st.selectbox("Sort tasks by:", ["Priority", "Time", "Status"])
    priority_order = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
    df['PriorityValue'] = df['Priority'].map(priority_order)

    if sort_by == "Priority":
        df = df.sort_values(by="PriorityValue", ascending=False)
    else:
        df = df.sort_values(by=sort_by)

    status_filter = st.multiselect("Filter by status:", df['Status'].unique())
    if status_filter:
        df = df[df['Status'].isin(status_filter)]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📝 Your To-Do List")
        st.dataframe(df.drop(columns="PriorityValue"))

    # Smart Suggestion
    with col2:
        st.subheader("🧠 Smart Suggestion")
        critical_tasks = df[df['Priority'] == 'Critical']
        if not critical_tasks.empty:
            top_task = critical_tasks.iloc[0]['Task']
            st.error(f"⚠️ FOCUS ON THIS: **{top_task}**")
            st.write("Reason: You marked this as Critical.")
        else:
            st.success("You are doing great! No critical alerts.")

    # Task Management
    st.write("---")
    task_to_manage = st.selectbox("Select a task to update/remove:", df['Task'])

    colA, colB, colC = st.columns(3)
    with colA:
        if st.button("Mark as Done"):
            for t in st.session_state.tasks:
                if t['Task'] == task_to_manage:
                    t['Status'] = "Done"
            pd.DataFrame(st.session_state.tasks).to_csv(TASKS_FILE, index=False)
            st.rerun()

    with colB:
        if st.button("Mark as In Progress"):
            for t in st.session_state.tasks:
                if t['Task'] == task_to_manage:
                    t['Status'] = "In Progress"
            pd.DataFrame(st.session_state.tasks).to_csv(TASKS_FILE, index=False)
            st.rerun()

    with colC:
        if st.button("Remove Task"):
            st.session_state.tasks = [t for t in st.session_state.tasks if t['Task'] != task_to_manage]
            pd.DataFrame(st.session_state.tasks).to_csv(TASKS_FILE, index=False)
            st.rerun()

    # Analytics
    st.write("---")
    st.subheader("📊 Task Analytics")
    st.bar_chart(df['Priority'].value_counts())

else:
    st.info("No tasks yet! Use the sidebar to add one.")

# --- Focus Timer ---
st.write("---")
st.subheader("⏱️ Focus Timer")
minutes = st.number_input("Set timer (minutes)", min_value=1, value=25)

if st.button("Start Timer"):
    progress_bar = st.progress(0)
    status_text = st.empty()

    end_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
    total_seconds = minutes * 60

    while datetime.datetime.now() < end_time:
        remaining = (end_time - datetime.datetime.now()).seconds
        percent_complete = int((total_seconds - remaining) / total_seconds * 100)
        progress_bar.progress(percent_complete)
        status_text.text(f"Focusing... {remaining//60} min {remaining%60} sec left")
        time.sleep(1)

    st.balloons()
    st.success("Time's up! Take a break.")
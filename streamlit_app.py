import streamlit as st
from datetime import datetime, timedelta

st.title("✅ Dead-Simple Tasks")

# Initialize storage for tasks if it doesn't exist
if 'tasks' not in st.session_state:
    st.session_state.tasks = [
        {"name": "Gym", "due": "2026-03-01"},
        {"name": "Rent", "due": "2026-03-11"}
    ]

# --- Input Section ---
task_name = st.text_input("Task name", placeholder="e.g., Water Plants")
days = st.number_input("Repeat every (days)", min_value=1, value=7)

if st.button("Add Task"):
    if task_name:
        # Calculate due date based on today + repeat days
        due_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        new_task = {"name": task_name, "due": due_date}
        st.session_state.tasks.append(new_task)
        st.success(f"Added {task_name}!")
    else:
        st.error("Please enter a task name.")

st.divider()

# --- Your Schedule Section ---
st.subheader("Your Schedule")

if st.session_state.tasks:
    for task in st.session_state.tasks:
        st.write(f"{task['name']} (Due: {task['due']})")
else:
    st.write("No tasks yet! Add one above.")

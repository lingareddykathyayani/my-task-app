import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Dead-Simple Tasks", page_icon="✅")

st.title("✅ Dead-Simple Tasks")

# 1. Initialize storage
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# 2. --- Callback Function to Add Task and Clear Input ---
def add_task():
    # Get values using the keys we assigned to the widgets
    name = st.session_state.new_task_input
    days = st.session_state.new_task_days
    
    if name:
        due_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        st.session_state.tasks.append({"name": name, "due": due_date})
        # Clear the input box by resetting its key
        st.session_state.new_task_input = ""
    else:
        st.warning("Please enter a task name.")

# 3. --- Input Section ---
# Assign keys and use the 'on_click' parameter
st.text_input("Task name", placeholder="e.g., Water Plants", key="new_task_input")
st.number_input("Repeat every (days)", min_value=1, value=7, key="new_task_days")

st.button("Add Task", use_container_width=True, on_click=add_task)

st.divider()

# 4. --- Your Schedule Section ---
st.subheader("Your Schedule")

if not st.session_state.tasks:
    st.info("No tasks yet! Add one above.")

for index, task in enumerate(st.session_state.tasks):
    col1, col2 = st.columns([4, 1]) 
    with col1:
        st.write(f"**{task['name']}** (Due: {task['due']})")
    with col2:
        if st.button("Done", key=f"btn_{index}"):
            st.session_state.tasks.pop(index)
            st.rerun()

# 5. --- Clear All Section ---
if st.session_state.tasks:
    st.write("") 
    if st.button("Clear All Tasks", type="secondary", use_container_width=True):
        st.session_state.tasks = []
        st.rerun()

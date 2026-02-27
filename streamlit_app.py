import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Dead-Simple Tasks", page_icon="✅")

st.title("✅ Dead-Simple Tasks")

# 1. Initialize storage
if 'tasks' not in st.session_state:
    st.session_state.tasks = [
        {"name": "Gym", "due": "2026-03-01"},
        {"name": "Rent", "due": "2026-03-11"}
    ]

# 2. --- Input Section ---
task_name = st.text_input("Task name", placeholder="e.g., Water Plants")
days = st.number_input("Repeat every (days)", min_value=1, value=7)

if st.button("Add Task", use_container_width=True):
    if task_name:
        due_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        st.session_state.tasks.append({"name": task_name, "due": due_date})
        st.rerun() # Refresh to show new task immediately
    else:
        st.warning("Please enter a task name.")

st.divider()

# 3. --- Your Schedule Section ---
st.subheader("Your Schedule")

if not st.session_state.tasks:
    st.info("All caught up! No tasks left.")

# Use a copy of the list to avoid errors while deleting
for index, task in enumerate(st.session_state.tasks):
    col1, col2 = st.columns([0, 1]) # Create two columns
    
    with col1:
        # Create a unique key for every button using the index
        if st.button("Done", key=f"btn_{index}"):
            st.session_state.tasks.pop(index)
            st.rerun() # Refresh to remove the item from UI
            
    with col2:
        st.write(f"**{task['name']}** (Due: {task['due']})")

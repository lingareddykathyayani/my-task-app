import streamlit as st
import json
import os
from datetime import datetime, timedelta

# --- 1. File to store data ---
SAVE_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks():
    with open(SAVE_FILE, "w") as f:
        json.dump(st.session_state.tasks, f)

# --- 2. Setup ---
st.set_page_config(page_title="Dead-Simple Tasks", page_icon="✅")
st.title("✅ Dead-Simple Tasks")

# Load existing tasks into session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = load_tasks()

# --- 3. Callback Function ---
def add_task_callback():
    name = st.session_state.new_task_input
    days = st.session_state.new_task_days
    
    if name:
        due_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        st.session_state.tasks.append({"name": name, "due": due_date})
        save_tasks() # Save to file immediately
        st.session_state.new_task_input = "" # Clear input
    else:
        st.warning("Please enter a task name.")

# --- 4. Input UI ---
st.text_input("Task name", placeholder="e.g., Water Plants", key="new_task_input")
st.number_input("Repeat every (days)", min_value=1, value=7, key="new_task_days")
st.button("Add Task", use_container_width=True, on_click=add_task_callback)

st.divider()

# --- 5. Your Schedule UI ---
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
            save_tasks() # Save updated list to file
            st.rerun()

# --- 6. Clear All ---
if st.session_state.tasks:
    st.write("") 
    if st.button("Clear All Tasks", type="secondary", use_container_width=True):
        st.session_state.tasks = []
        save_tasks() # Clear file
        st.rerun()

import streamlit as st
import json
import os
from datetime import datetime, timedelta

# --- 1. Persistence Logic ---
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

# INITIALIZE SESSION STATE KEYS
if 'tasks' not in st.session_state:
    st.session_state.tasks = load_tasks()

# This part fixes the error: set the default value here instead of in the widget
if 'new_task_days' not in st.session_state:
    st.session_state.new_task_days = 7

# --- 3. Add Task Callback ---
def add_task_callback():
    name = st.session_state.new_task_input
    days = st.session_state.new_task_days
    
    if name:
        due_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        st.session_state.tasks.append({"name": name, "due": due_date})
        
        # Sort by date
        st.session_state.tasks = sorted(st.session_state.tasks, key=lambda x: x['due'])
        save_tasks()
        
        # CLEAR LOGIC: This now works without error
        st.session_state.new_task_input = "" 
        st.session_state.new_task_days = 7
    else:
        st.warning("Please enter a task name.")

# --- 4. Input UI ---
st.text_input("Task name", placeholder="e.g., Water Plants", key="new_task_input")

# FIXED: Removed 'value=7' and used the Session State key instead
st.number_input("Repeat every (days)", min_value=1, key="new_task_days")

st.button("Add Task", use_container_width=True, on_click=add_task_callback)

st.divider()

# --- 5. Your Schedule UI ---
st.subheader("Your Schedule")

if not st.session_state.tasks:
    st.info("No tasks yet! Add one above.")
else:
    for index, task in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([4, 1]) 
        with col1:
            st.write(f"**{task['name']}** (Due: {task['due']})")
        with col2:
            if st.button("Done", key=f"btn_{index}"):
                st.session_state.tasks.pop(index)
                save_tasks()
                st.rerun()

# --- 6. Clear All ---
if st.session_state.tasks:
    if st.button("Clear All Tasks", type="secondary", use_container_width=True):
        st.session_state.tasks = []
        save_tasks()
        st.rerun()


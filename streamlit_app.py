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

if 'tasks' not in st.session_state:
    st.session_state.tasks = load_tasks()

if 'new_task_days' not in st.session_state:
    st.session_state.new_task_days = 7

# --- 3. Callbacks ---
def add_task_callback():
    name = st.session_state.new_task_input
    days = st.session_state.new_task_days
    
    if name:
        # Calculate initial due date
        due_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        # We now store 'interval' so we know how many days to add later
        st.session_state.tasks.append({"name": name, "due": due_date, "interval": days})
        
        # Sort and Save
        st.session_state.tasks = sorted(st.session_state.tasks, key=lambda x: x['due'])
        save_tasks()
        
        # Clear inputs
        st.session_state.new_task_input = "" 
        st.session_state.new_task_days = 7
    else:
        st.warning("Please enter a task name.")

def complete_task(index):
    task = st.session_state.tasks[index]
    # Calculate NEW due date: Today + the original interval
    new_date = (datetime.now() + timedelta(days=task['interval'])).strftime('%Y-%m-%d')
    st.session_state.tasks[index]['due'] = new_date
    
    # Re-sort so the new date moves to the bottom of the list
    st.session_state.tasks = sorted(st.session_state.tasks, key=lambda x: x['due'])
    save_tasks()

# --- 4. Input UI ---
st.text_input("Task name", placeholder="e.g., Water Plants", key="new_task_input")
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
            # Highlight if due today or earlier
            is_overdue = task['due'] <= datetime.now().strftime('%Y-%m-%d')
            display_name = f"🚨 **{task['name']}**" if is_overdue else f"**{task['name']}**"
            st.write(f"{display_name} (Due: {task['due']})")
        with col2:
            # When "Done" is clicked, it calls the reschedule logic
            if st.button("Done", key=f"btn_{index}"):
                complete_task(index)
                st.rerun()

# --- 6. Clear All (For when you really want to delete) ---
if st.session_state.tasks:
    st.write("")
    if st.button("Delete All Tasks Permanently", type="secondary", use_container_width=True):
        st.session_state.tasks = []
        save_tasks()
        st.rerun()

import streamlit as st
from datetime import datetime, timedelta

st.title("✅ Dead-Simple Tasks")

# Input Section
task_name = st.text_input("Task name", placeholder="e.g., Water Plants")
days = st.number_input("Repeat every (days)", min_value=1, value=7)

if st.button("Add Task"):
    st.success(f"Added: {task_name}")

st.divider()

# Display Section
st.subheader("Your Schedule")
st.write("Gym (Due: 2026-03-01)")
st.write("Rent (Due: 2026-03-11)")

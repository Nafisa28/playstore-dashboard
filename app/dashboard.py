import streamlit as st
import runpy
import os

st.title("Google Play Store Data Analysis Dashboard")

st.sidebar.title("Select Task")

task = st.sidebar.radio(
    "Go to:",
    ("Task 1", "Task 2", "Task 3", "Task 4", "Task 5", "Task 6")
)

base_path = os.path.dirname(__file__)

if task == "Task 1":
    runpy.run_path(os.path.join(base_path, "task1_dashboard.py"))

elif task == "Task 2":
    runpy.run_path(os.path.join(base_path, "task2_map.py"))

elif task == "Task 3":
    runpy.run_path(os.path.join(base_path, "task3.py"))

elif task == "Task 4":
    runpy.run_path(os.path.join(base_path, "task4.py"))

elif task == "Task 5":
    runpy.run_path(os.path.join(base_path, "task5.py"))

elif task == "Task 6":
    runpy.run_path(os.path.join(base_path, "task6.py"))

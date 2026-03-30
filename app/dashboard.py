import streamlit as st

st.title("Google Play Store Data Analysis Dashboard")

st.sidebar.title("Select Task")

task = st.sidebar.radio(
    "Go to:",
    ("Task 1", "Task 2", "Task 3", "Task 4", "Task 5", "Task 6")
)

if task == "Task 1":
    import task1

elif task == "Task 2":
    import task2

elif task == "Task 3":
    import task3

elif task == "Task 4":
    import task4

elif task == "Task 5":
    import task5

elif task == "Task 6":
    import task6

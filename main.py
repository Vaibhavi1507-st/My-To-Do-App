# import libraries
import json
import os

import streamlit as st


FILE_NAME = "tasks.json"

# Connecting json

def load_tasks():
    if not os.path.exists(FILE_NAME) or os.path.getsize(FILE_NAME) == 0:
        with open(FILE_NAME, "w") as f:
            json.dump([], f)
        return []

    with open(FILE_NAME, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)


# Streamlit UI

st.title("My To-Do App")

tasks = load_tasks()
task_text = st.text_input("Enter task here")

if st.button("Add task"):
    if task_text.strip():
        new_task = {
            "id": len(tasks) + 1,
            "text": task_text.strip(),
            "status": "pending",
        }
        tasks.append(new_task)
        save_tasks(tasks)
        st.success("Task added.")
        st.rerun()
    else:
        st.warning("Please enter a task.")

st.subheader("Task List")

# Checkbox

if not tasks:
    st.info("No tasks yet.")
else:
    for task in tasks:
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            checked = task["status"] == "completed"
            new_status = st.checkbox(
                f"{task['id']}. {task['text']}",
                value=checked,
                key=f"task_{task['id']}",
            )

        if new_status != checked:
            task["status"] = "completed" if new_status else "pending"
            save_tasks(tasks)
            st.rerun()
# Delete Button
        with col2:
            if st.button("Delete", key=f"del_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()

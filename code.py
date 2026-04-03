import streamlit as st
st.set_page_config(page_title="Smart Task Manager", page_icon="✅")
st.info("🚀 Cloud-based Task Manager (Supabase connected)")
if "option" not in st.session_state:
    st.session_state.option = "View Tasks"

import os


from supabase import create_client

url = "https://fxivugwhlbhspxivzigf.supabase.co"
key = os.getenv("SUPABASE_KEY")


if key is None:
    st.error("Supabase key not found! Set SUPABASE_KEY environment variable.")
    st.stop()


supabase = create_client(url, key)

def get_tasks():
    response = supabase.table("tasks").select("*").execute()
    return response.data
tasks = get_tasks()



st.title("Smart Task Manager")
col1, col2, col3, col4 , col5, col6, col7= st.columns([2,2,2,2,2,2,2])

if col1.button("Add"):
    st.session_state.option = "Add Task"

if col2.button("View"):
    st.session_state.option = "View Tasks"

if col3.button("Delete"):
    st.session_state.option = "Delete Task"

if col4.button("Done"):
    st.session_state.option = "Mark Task as Completed"

if col5.button("Search"):
    st.session_state.option = "Search Task"

if col6.button("Pending"):
    st.session_state.option = "Show Pending Tasks"

if col7.button("Clear"):
    st.session_state.option = "Clear All Tasks"

option = st.session_state.option

if option == "Add Task":
    tasks = get_tasks()
    title = st.text_input("Enter your task:")
    priority = st.selectbox("Enter priority:", ["High", "Medium", "Low"])

    if st.button("Add Task"):
        
        if title.strip() == "":
            st.warning("Task cannot be empty!")
        elif any(task["title"].lower() == title.lower() for task in tasks):
            st.warning("Task already exists!")
        else:
            supabase.table("tasks").insert({
                "title": title,
                "status": "Pending",
                "priority": priority
            }).execute()

            st.success("Task added successfully!")
            st.rerun()
elif option=="View Tasks":
    
    if len(tasks)==0:
        st.write("No tasks for you!")
    else:
        total = len(tasks)
        completed = sum(1 for t in tasks if t["status"] == "Completed")
        pending = total - completed

        st.write(f"📊 Total: {total} | ✅ Completed: {completed} | ⏳ Pending: {pending}")
        st.write("Your tasks:")
        for i,task in enumerate(tasks):
            status_icon = "✅" if task["status"] == "Completed" else "⏳"
            st.markdown(f"**{i+1}👉 {task['title']}**  \n{status_icon} | Priority: `{task['priority']}`")
        
elif option=="Delete Task":
    
    if len(tasks) == 0:
        st.warning("No tasks to delete!")
    else:
        num = int(st.number_input("Enter task number:", min_value=1, max_value=len(tasks)))
        
        if st.button("Delete Task"):
            if 1 <= num <= len(tasks):
                task_id = tasks[num-1]["id"]
                supabase.table("tasks").delete().eq("id", task_id).execute()

                st.success("Task deleted successfully!")
                st.rerun()
        
            else:
                st.warning("Invalid task number!")
            

            
elif option=="Mark Task as Completed":
    
    if len(tasks) == 0:
        st.warning("No tasks to mark as completed!")
    else:
        num=int(st.number_input("Enter the task number to mark as completed:", min_value=1, max_value=len(tasks)))

        if st.button("Mark as Completed"):
            if 1 <= num <= len(tasks):
                task_id = tasks[num-1]["id"]

                supabase.table("tasks").update({
                    "status": "Completed"
                }).eq("id", task_id).execute()

                st.success("Task marked as completed!")
                st.rerun()
            else:
                st.write("Invalid task number!")
    
elif option == "Search Task":
    
    keyword = st.text_input("Enter keyword to search:")

    if keyword:
        response = supabase.table("tasks") \
            .select("*") \
            .ilike("title", f"%{keyword}%") \
            .execute()

        tasks = response.data

        if tasks:
            for i, task in enumerate(tasks):
                status_icon = "✅" if task["status"] == "Completed" else "⏳"
                st.markdown(f"**{i+1} 👉 {task['title']}**  \n{status_icon} | `{task['priority']}`")
            
        else:
            st.write("No matching tasks found.")
elif option == "Show Pending Tasks":
    
    response = supabase.table("tasks").select("*").eq("status", "Pending").execute()
    tasks = response.data

    if tasks:
        for i, task in enumerate(tasks):
            st.markdown(f"**{i+1} 👉 {task['title']}**  \n⏳ | `{task['priority']}`")
            
    else:
        st.write("No pending tasks 🎉")
elif option == "Clear All Tasks":
    
    confirm = st.checkbox("Are you sure you want to delete all tasks?")

    if st.button("Clear All Tasks"):
        if confirm:
            supabase.table("tasks").delete().neq("id", 0).execute()
            st.success("All tasks cleared!")
            st.rerun()
        else:
            st.warning("Please confirm before clearing!")
else:
    st.write("Invalid choice! Please try again.")





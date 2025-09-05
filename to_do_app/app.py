import tkinter as tk
from tkinter import messagebox, ttk
import os
from datetime import datetime

FILE_NAME = "tasks.txt"

# ----------------------- Logic Functions -----------------------
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            tasks = file.readlines()
        for line in tasks:
            line = line.strip()
            parts = line.split("||")
            if len(parts) == 4:
                completed, task_text, priority, due_date = parts
                tasks_data.append({
                    "completed": completed == "1",
                    "text": task_text,
                    "priority": priority,
                    "due_date": due_date
                })
        refresh_listbox()

def save_tasks():
    with open(FILE_NAME, "w") as file:
        for task in tasks_data:
            line = f"{int(task['completed'])}||{task['text']}||{task['priority']}||{task['due_date']}\n"
            file.write(line)

def get_color(task):
    if task["completed"]:
        return "gray"
    if task["priority"] == "High":
        return "#e74c3c"  # red
    elif task["priority"] == "Medium":
        return "#f39c12"  # orange
    else:
        return "#2ecc71"  # green

def refresh_listbox(filtered_tasks=None):
    tasks_listbox.delete(0, tk.END)
    display_tasks = filtered_tasks if filtered_tasks is not None else tasks_data
    for task in display_tasks:
        tasks_listbox.insert(tk.END, task["text"])
        tasks_listbox.itemconfig(tk.END, fg=get_color(task))

def add_task():
    task_text = task_entry.get()
    priority = priority_var.get()
    due_date = due_date_entry.get()
    if task_text:
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Invalid Date", "Date must be YYYY-MM-DD")
                return
        else:
            due_date = ""
        tasks_data.append({
            "completed": False,
            "text": task_text,
            "priority": priority,
            "due_date": due_date
        })
        task_entry.delete(0, tk.END)
        due_date_entry.delete(0, tk.END)
        refresh_listbox()
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Enter a task!")

def delete_task():
    try:
        index = tasks_listbox.curselection()[0]
        tasks_data.pop(index)
        refresh_listbox()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to delete!")

def mark_completed():
    try:
        index = tasks_listbox.curselection()[0]
        tasks_data[index]["completed"] = True
        refresh_listbox()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to mark completed!")

def edit_task():
    try:
        index = tasks_listbox.curselection()[0]
        task_text = task_entry.get()
        priority = priority_var.get()
        due_date = due_date_entry.get()
        if not task_text:
            messagebox.showwarning("Warning", "Enter task text!")
            return
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Invalid Date", "Date must be YYYY-MM-DD")
                return
        else:
            due_date = ""
        tasks_data[index].update({"text": task_text, "priority": priority, "due_date": due_date})
        task_entry.delete(0, tk.END)
        due_date_entry.delete(0, tk.END)
        refresh_listbox()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to edit!")

def move_up():
    try:
        index = tasks_listbox.curselection()[0]
        if index > 0:
            tasks_data[index], tasks_data[index-1] = tasks_data[index-1], tasks_data[index]
            refresh_listbox()
            tasks_listbox.select_set(index-1)
            save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to move!")

def move_down():
    try:
        index = tasks_listbox.curselection()[0]
        if index < len(tasks_data)-1:
            tasks_data[index], tasks_data[index+1] = tasks_data[index+1], tasks_data[index]
            refresh_listbox()
            tasks_listbox.select_set(index+1)
            save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to move!")

def clear_tasks():
    global tasks_data
    tasks_data = []
    refresh_listbox()
    save_tasks()

def filter_tasks():
    priority_filter = filter_priority_var.get()
    status_filter = filter_status_var.get()
    filtered = tasks_data
    if priority_filter != "All":
        filtered = [t for t in filtered if t["priority"] == priority_filter]
    if status_filter != "All":
        if status_filter == "Completed":
            filtered = [t for t in filtered if t["completed"]]
        else:
            filtered = [t for t in filtered if not t["completed"]]
    refresh_listbox(filtered)

def search_tasks(event=None):
    query = search_entry.get().lower()
    if query:
        filtered = [t for t in tasks_data if query in t["text"].lower()]
        refresh_listbox(filtered)
    else:
        refresh_listbox()

def sort_tasks():
    sort_by = sort_var.get()
    if sort_by == "Priority":
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        tasks_data.sort(key=lambda x: priority_order[x["priority"]])
    elif sort_by == "Due Date":
        tasks_data.sort(key=lambda x: x["due_date"] if x["due_date"] else "9999-99-99")
    refresh_listbox()
    save_tasks()

# ----------------------- GUI Setup -----------------------
root = tk.Tk()
root.title("Themed Professional To-Do List")
root.geometry("720x600")
root.configure(bg="#34495e")  # dark background

tasks_data = []

# Entry frame
entry_frame = tk.Frame(root, bg="#34495e")
entry_frame.pack(pady=10)

task_entry = tk.Entry(entry_frame, width=30, font=("Helvetica", 12))
task_entry.grid(row=0, column=0, padx=5)

due_date_entry = tk.Entry(entry_frame, width=12, font=("Helvetica", 12))
due_date_entry.grid(row=0, column=1, padx=5)
due_date_entry.insert(0, "YYYY-MM-DD")

priority_var = tk.StringVar(value="Medium")
priority_menu = ttk.Combobox(entry_frame, textvariable=priority_var, values=["Low","Medium","High"], width=10, state="readonly")
priority_menu.grid(row=0, column=2, padx=5)

# Buttons frame
btn_frame = tk.Frame(root, bg="#34495e")
btn_frame.pack(pady=5)

btn_style = {"font":("Helvetica",11), "bg":"#1abc9c", "fg":"white", "activebackground":"#16a085", "width":14, "bd":0}

tk.Button(btn_frame, text="Add Task", command=add_task, **btn_style).grid(row=0,column=0,padx=5,pady=5)
tk.Button(btn_frame, text="Edit Task", command=edit_task, **btn_style).grid(row=0,column=1,padx=5,pady=5)
tk.Button(btn_frame, text="Delete Task", command=delete_task, **btn_style).grid(row=0,column=2,padx=5,pady=5)
tk.Button(btn_frame, text="Mark Completed", command=mark_completed, **btn_style).grid(row=1,column=0,padx=5,pady=5)
tk.Button(btn_frame, text="Move Up", command=move_up, **btn_style).grid(row=1,column=1,padx=5,pady=5)
tk.Button(btn_frame, text="Move Down", command=move_down, **btn_style).grid(row=1,column=2,padx=5,pady=5)
tk.Button(root, text="Clear All Tasks", command=clear_tasks, **btn_style).pack(pady=10)

# Filter/search frame
filter_frame = tk.Frame(root, bg="#34495e")
filter_frame.pack(pady=5)

filter_priority_var = tk.StringVar(value="All")
filter_priority_menu = ttk.Combobox(filter_frame, textvariable=filter_priority_var, values=["All","Low","Medium","High"], width=10, state="readonly")
filter_priority_menu.grid(row=0,column=0,padx=5)
filter_priority_menu.bind("<<ComboboxSelected>>", lambda e: filter_tasks())

filter_status_var = tk.StringVar(value="All")
filter_status_menu = ttk.Combobox(filter_frame, textvariable=filter_status_var, values=["All","Completed","Pending"], width=10, state="readonly")
filter_status_menu.grid(row=0,column=1,padx=5)
filter_status_menu.bind("<<ComboboxSelected>>", lambda e: filter_tasks())

search_entry = tk.Entry(filter_frame, width=20, font=("Helvetica", 12))
search_entry.grid(row=0,column=2,padx=5)
search_entry.bind("<KeyRelease>", search_tasks)

sort_var = tk.StringVar(value="None")
sort_menu = ttk.Combobox(filter_frame, textvariable=sort_var, values=["None","Priority","Due Date"], width=12, state="readonly")
sort_menu.grid(row=0,column=3,padx=5)
sort_menu.bind("<<ComboboxSelected>>", lambda e: sort_tasks())

# Listbox
tasks_listbox = tk.Listbox(root, width=90, height=20, font=("Helvetica", 12), bd=0, selectbackground="#1abc9c", activestyle="none")
tasks_listbox.pack(pady=10)

# Load tasks
load_tasks()

root.mainloop()

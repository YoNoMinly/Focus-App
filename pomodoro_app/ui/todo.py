import tkinter as tk
from tkinter import simpledialog

class TodoFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#1e1e1e")

        self.tasks = []


        top_bar = tk.Frame(self, bg="#1e1e1e")
        top_bar.pack(fill="x", pady=(5, 0), padx=10)

        title = tk.Label(top_bar, text="To-Do List", fg="white", bg="#1e1e1e", font=("Helvetica", 14, "bold"))
        title.pack(side="left")

        add_btn = tk.Button(top_bar, text="+", command=self.add_task_dialog, bg="#1e1e1e", fg="white", width=3)
        add_btn.pack(side="right")


        self.task_container = tk.Frame(self, bg="#1e1e1e")
        self.task_container.pack(fill="both", expand=True, padx=10, pady=10)

    def get_data(self):
        return self.tasks

    def set_data(self, data):
        self.tasks = data
        for task in self.tasks:
            self.listbox.insert(tk.END, task["text"])
    
    def add_task_dialog(self):
        task_text = simpledialog.askstring("New goal", "New goal title:")
        if task_text:
            self.add_task(task_text)

    def add_task(self, text):
        task_frame = tk.Frame(self.task_container, bg="#1e1e1e")
        task_frame.pack(fill="x", pady=3)

        var = tk.BooleanVar()
        check = tk.Checkbutton(
            task_frame, variable=var, command=lambda: self.toggle_task_color(label, var),
            bg="#1e1e1e", activebackground="#1e1e1e", highlightthickness=0,
            selectcolor="#FFFFFF"
        )
        
        check.pack(side="left")

        label = tk.Label(task_frame, text=text, fg="red", bg="#1e1e1e", font=("Helvetica", 12), anchor="w")
        label.pack(side="left", fill="x", expand=True, padx=5)

        delete_btn = tk.Button(task_frame, text="x", command=lambda: self.remove_task(task_frame),
                               bg="#111111", fg="white", width=2)
        delete_btn.pack(side="right", padx=5)

        self.tasks.append((task_frame, label, var))

    def toggle_task_color(self, label, var):
        label.config(fg="#00FF00" if var.get() else "#FF0000")

    def remove_task(self, task_frame):
        task_frame.destroy()

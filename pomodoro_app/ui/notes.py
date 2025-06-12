import tkinter as tk
from tkinter import messagebox, simpledialog

class NotesFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#1e1e1e", bd=1, relief="sunken")

        self.notes = {}

        left_frame = tk.Frame(self, bg="#1e1e1e")
        left_frame.pack(side="left", fill="y", padx=(10,5), pady=5)


        self.top_btn_frame = tk.Frame(left_frame, bg="#1e1e1e")
        self.top_btn_frame.pack(fill="x")

        self.add_btn = tk.Button(self.top_btn_frame, text="+", command=self.add_note,
                                 bg="#333", fg="white", width=2, font=("Helvetica", 14, "bold"))
        self.add_btn.pack(side="right", padx=2)

        self.del_btn = tk.Button(self.top_btn_frame, text="✖", command=self.delete_note,
                                 bg="#cc3333", fg="white", width=2, font=("Helvetica", 14, "bold"))
        self.del_btn.pack(side="right", padx=2)

        self.close_btn = tk.Button(self.top_btn_frame, text="-", command=self.close_note,
                                   bg="#555", fg="white", width=2, font=("Helvetica", 14, "bold"))
        self.close_btn.pack(side="right", padx=2)

        self.listbox = tk.Listbox(left_frame, width=25, height=15, bg="#222222", fg="white",
                                  selectbackground="#00cc66", selectforeground="black", font=("Helvetica", 12))
        self.listbox.pack(side="left", fill="y", pady=5)

        scrollbar = tk.Scrollbar(left_frame, command=self.listbox.yview)
        scrollbar.pack(side="left", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.note_frame = tk.Frame(self, bg="#1e1e1e", width=300, height=200)
        self.note_frame.pack_propagate(False)  
        self.note_frame.pack(side="right", fill="both", expand=True, padx=(5,10), pady=5)

        self.text = tk.Text(self.note_frame, bg="#222222", fg="white", insertbackground="white", font=("Helvetica", 12))
        self.text.pack(fill="both", expand=True)

        self.text.bind("<FocusOut>", self.save_note)

        self.current_note = None


        self.text.pack_forget()
        self.del_btn.config(state="disabled")
        self.close_btn.config(state="disabled")

    def get_data(self):
        return self.text.get("1.0", tk.END).strip()

    def set_data(self, data):
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, data)

    def add_note(self):
        title = simpledialog.askstring("New note", "enter new note:", parent=self)
        if title:
            if title in self.notes:
                messagebox.showerror("error", "such title already exist!")
                return
            self.notes[title] = ""
            self.listbox.insert(tk.END, title)
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(tk.END)
            self.on_select()

    def delete_note(self):
        if not self.current_note:
            return
        if messagebox.askyesno("Delete", f"Delete note '{self.current_note}'?"):
            idx = self.listbox.get(0, tk.END).index(self.current_note)
            self.listbox.delete(idx)
            self.notes.pop(self.current_note, None)
            self.current_note = None
            self.text.delete("1.0", tk.END)
            self.text.pack_forget()
            self.del_btn.config(state="disabled")
            self.close_btn.config(state="disabled")

    def close_note(self):
        self.save_note()
        self.current_note = None
        self.text.delete("1.0", tk.END)
        self.text.pack_forget()
        self.listbox.selection_clear(0, tk.END)
        self.del_btn.config(state="disabled")
        self.close_btn.config(state="disabled")

    def on_select(self, event=None):
        selection = self.listbox.curselection()
        if not selection:
            self.current_note = None
            self.text.pack_forget()
            self.del_btn.config(state="disabled")
            self.close_btn.config(state="disabled")
            return
        idx = selection[0]
        title = self.listbox.get(idx)
        self.current_note = title
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, self.notes.get(title, ""))
        self.text.pack(fill="both", expand=True)
        self.del_btn.config(state="normal")
        self.close_btn.config(state="normal")

    def save_note(self, event=None):
        if self.current_note:
            self.notes[self.current_note] = self.text.get("1.0", tk.END).rstrip()

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#121212")
    root.geometry("600x400")
    nf = NotesFrame(root)
    nf.pack(fill="both", expand=True)
    root.mainloop()

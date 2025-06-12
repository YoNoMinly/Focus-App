import tkinter as tk

class TimerFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#1e1e1e")
        
        self.default_time_sec = 25 * 60  
        self.remaining = self.default_time_sec
        self.running = False
        
        self.time_var = tk.StringVar()
        self.update_time_var()
        
        time_controls = tk.Frame(self, bg="#1e1e1e")
        time_controls.pack(pady=10)
        

        left_buttons_frame = tk.Frame(time_controls, bg="#1e1e1e")
        left_buttons_frame.pack(side="left", padx=10)
        
        left_btns = []
        left_labels = []
        self.intervals = [1, 3, 5]
        for interval in self.intervals:
            btn = tk.Button(left_buttons_frame, text="←", command=lambda i=interval: self.change_time(-i),
                            bg="#111111", fg="white", width=3, font=("Helvetica", 14))
            btn.grid(row=0, column=self.intervals.index(interval), padx=5)
            left_btns.append(btn)
            lbl = tk.Label(left_buttons_frame, text=str(interval), fg="white", bg="#1e1e1e", font=("Helvetica", 12))
            lbl.grid(row=1, column=self.intervals.index(interval), padx=5)
            left_labels.append(lbl)
        

        self.time_label = tk.Label(time_controls, textvariable=self.time_var, fg="white", bg="#1e1e1e",
                                   font=("Helvetica", 36), width=5)
        self.time_label.pack(side="left", padx=10)
        

        right_buttons_frame = tk.Frame(time_controls, bg="#1e1e1e")
        right_buttons_frame.pack(side="left", padx=10)
        
        right_btns = []
        right_labels = []
        for interval in self.intervals:
            btn = tk.Button(right_buttons_frame, text="→", command=lambda i=interval: self.change_time(i),
                            bg="#111111", fg="white", width=3, font=("Helvetica", 14))
            btn.grid(row=0, column=self.intervals.index(interval), padx=5)
            right_btns.append(btn)
            lbl = tk.Label(right_buttons_frame, text=str(interval), fg="white", bg="#1e1e1e", font=("Helvetica", 12))
            lbl.grid(row=1, column=self.intervals.index(interval), padx=5)
            right_labels.append(lbl)
        

        self.progress_bg = tk.Frame(self, bg="#222222", height=20, width=300)
        self.progress_bg.pack(pady=(10, 10))
        self.progress_bar = tk.Frame(self.progress_bg, bg="#00cc66", height=20, width=0)
        self.progress_bar.pack(side="left", fill="y")
        

        self.start_pause_button = tk.Button(self, text="Start", command=self.toggle_timer,
                                            bg="#111111", fg="white", width=10)
        self.start_pause_button.pack(pady=5)
        
        self.after_id = None
        
    def update_time_var(self):
        m, s = divmod(self.remaining, 60)
        self.time_var.set(f"{m:02d}:{s:02d}")
        
    def change_time(self, delta_min):
        if self.running:
            return
        new_time = self.default_time_sec + delta_min * 60
        if new_time < 60:
            new_time = 60
        elif new_time > 99 * 60:
            new_time = 99 * 60
        self.default_time_sec = new_time
        self.remaining = self.default_time_sec
        self.update_time_var()
        self.update_progress()
        
    def toggle_timer(self):
        if self.running:
            self.pause_timer()
        else:
            self.start_timer()
            
    def start_timer(self):
        if self.remaining > 0:
            self.running = True
            self.start_pause_button.config(text="Pause")
            self.countdown()
        
    def pause_timer(self):
        self.running = False
        self.start_pause_button.config(text="Start")
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
            
    def countdown(self):
        if self.running and self.remaining > 0:
            self.remaining -= 1
            self.update_time_var()
            self.update_progress()
            self.after_id = self.after(1000, self.countdown)
        elif self.remaining == 0:
            self.running = False
            self.start_pause_button.config(text="Start")
        
    def update_progress(self):
        percent = (self.default_time_sec - self.remaining) / self.default_time_sec
        width = int(300 * percent)
        self.progress_bar.config(width=width)
        
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#1e1e1e")
    root.geometry("500x220")
    timer = TimerFrame(root)
    timer.pack(fill="both", expand=True)
    root.mainloop()

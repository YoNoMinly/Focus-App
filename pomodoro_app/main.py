import tkinter as tk
import json
import os
from ui.timer import TimerFrame
from ui.todo import TodoFrame
from ui.notes import NotesFrame
from ui.canvas import WeatherCanvas


DATA_FILE = "data.json"

def main():
    root = tk.Tk()
    root.title("focus_app")
    root.geometry("1200x600")
    root.configure(bg="#1e1e1e")

    dark_mode = True

    timer = TimerFrame(root)
    timer.pack(fill="x", pady=10, padx=10)

    content = tk.Frame(root, bg="#1e1e1e")
    content.pack(fill="both", expand=True, padx=10, pady=10)

    notes = NotesFrame(content)
    notes.pack(side="left", fill="both", expand=True, padx=(0, 10))


    weather_panel = tk.Frame(content, bg="#1e1e1e")
    weather_panel.pack(side="right", fill="y", padx=(10, 0))

    weather_canvas = WeatherCanvas(weather_panel, width=300, height=300, bg="#1e1e1e", highlightthickness=0)
    weather_canvas.pack(fill="both", expand=True, pady=(0, 10))


    right_panel = tk.Frame(content, bg="#1e1e1e")
    right_panel.pack(side="right", fill="both", expand=True, padx=(0, 10))

        # Додати панель кнопок під canvas
    weather_buttons = tk.Frame(weather_panel, bg="#1e1e1e")
    weather_buttons.pack(fill="x")

    def set_clear():
        weather_canvas.set_weather("clear")

    def set_rain():
        weather_canvas.set_weather("rain")

    def set_snow():
        weather_canvas.set_weather("snow")

    btn_clear = tk.Button(weather_buttons, text="clear", command=set_clear, bg="#444444", fg="white")
    btn_clear.pack(side="left", expand=True, fill="x", padx=2)

    btn_rain = tk.Button(weather_buttons, text="rain", command=set_rain, bg="#444444", fg="white")
    btn_rain.pack(side="left", expand=True, fill="x", padx=2)

    btn_snow = tk.Button(weather_buttons, text="snow", command=set_snow, bg="#444444", fg="white")
    btn_snow.pack(side="left", expand=True, fill="x", padx=2)

    todo = TodoFrame(right_panel)
    todo.pack(fill="both", expand=True, pady=(0, 10))

    def toggle_theme():
        nonlocal dark_mode
        dark_mode = not dark_mode
        apply_theme()

    theme_button = tk.Button(right_panel, text="change theme", command=toggle_theme, bg="#444444", fg="white")
    theme_button.pack(fill="x")

    def apply_theme():
        bg = "#0A0A0A" if dark_mode else "#444444"
        fg = "white" if dark_mode else "black"

        root.configure(bg=bg)
        content.configure(bg=bg)
        right_panel.configure(bg=bg)
        weather_panel.configure(bg=bg)

        timer.configure(bg=bg)
        if hasattr(timer, "apply_theme"):
            timer.apply_theme(dark_mode)

        notes.configure(bg=bg)
        if hasattr(notes, "apply_theme"):
            notes.apply_theme(dark_mode)

        todo.configure(bg=bg)
        if hasattr(todo, "apply_theme"):
            todo.apply_theme(dark_mode)

        theme_button.configure(bg=bg, fg=fg, activebackground=bg, activeforeground=fg)

    def save_data():
        data = {
            "notes": notes.get_data() if hasattr(notes, "get_data") else [],
            "todo": todo.get_data() if hasattr(todo, "get_data") else [],
            "dark_mode": dark_mode
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("save")

    def load_data():
        nonlocal dark_mode
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "timer" in data and hasattr(timer, "set_data"):
                    timer.set_data(data["timer"])
                if "notes" in data and hasattr(notes, "set_data"):
                    notes.set_data(data["notes"])
                if "todo" in data and hasattr(todo, "set_data"):
                    todo.set_data(data["todo"])
                dark_mode = data.get("dark_mode", True)
            print("download")
        else:
            print("no file to download")

    def on_closing():
        save_data()
        root.destroy()

    load_data()
    apply_theme()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

if __name__ == "__main__":
    main()

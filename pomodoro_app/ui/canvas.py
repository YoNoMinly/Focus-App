import tkinter as tk
import time
import random

class WeatherCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.weather = "clear"
        self.drops = []
        self.snowflakes = []
        self.after_id = None
        self.animate()

    def set_weather(self, weather):
        self.weather = weather
        self.drops.clear()
        self.snowflakes.clear()

    def is_night(self):
        hour = time.localtime().tm_hour
        return hour < 6 or hour >= 20

    def get_sky_color(self):
        hour = time.localtime().tm_hour
        if 6 <= hour < 9:
            return "#FFA500"
        elif 9 <= hour < 17:
            return "#87CEEB"
        elif 17 <= hour < 20:
            return "#FF4500"
        else:
            return "#001830"

    def draw_moon(self):
        w = self.winfo_width()
        h = self.winfo_height()
        moon_x = int(w * 0.8)
        moon_y = int(h * 0.3)
        moon_radius = 50

        self.create_oval(moon_x - moon_radius, moon_y - moon_radius,
                         moon_x + moon_radius, moon_y + moon_radius,
                         fill="#FDF6E3", outline="")

        offset = 15
        self.create_oval(moon_x - moon_radius + offset, moon_y - moon_radius,
                         moon_x + moon_radius + offset, moon_y + moon_radius,
                         fill=self.get_sky_color(), outline="")

    def animate(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        self.create_rectangle(0, 0, w, h, fill=self.get_sky_color(), outline="")

        if self.is_night():
            self.draw_moon()
        if self.weather == "rain":
            self.animate_rain(w, h)
        elif self.weather == "snow":
            self.animate_snow(w, h)

        self.after_id = self.after(50, self.animate)

    def animate_rain(self, w, h):
        while len(self.drops) < 150:
            x = random.randint(0, w)
            y = random.randint(-h, 0)
            length = random.randint(10, 20)
            speed = random.uniform(7, 10)
            self.drops.append({"x": x, "y": y, "length": length, "speed": speed})

        for drop in self.drops:
            drop["y"] += drop["speed"]
            if drop["y"] > h:
                drop["y"] = random.randint(-20, 0)
                drop["x"] = random.randint(0, w)
            self.create_line(drop["x"], drop["y"], drop["x"], drop["y"] + drop["length"], fill="#0cf")

    def animate_snow(self, w, h):
        while len(self.snowflakes) < 50:
            x = random.randint(0, w)
            y = random.randint(-h, 0)
            size = random.randint(2, 5)
            speed = random.uniform(1, 3)
            self.snowflakes.append({"x": x, "y": y, "size": size, "speed": speed, "dx": random.uniform(-0.5, 0.5)})

        for flake in self.snowflakes:
            flake["y"] += flake["speed"]
            flake["x"] += flake["dx"]
            if flake["y"] > h:
                flake["y"] = random.randint(-20, 0)
                flake["x"] = random.randint(0, w)
            if flake["x"] < 0:
                flake["x"] = w
            elif flake["x"] > w:
                flake["x"] = 0
            self.create_oval(flake["x"], flake["y"], flake["x"] + flake["size"], flake["y"] + flake["size"], fill="white", outline="")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Погода у вікні")
    width, height = 600, 600
    root.geometry(f"{width}x{height}")


    root.grid_rowconfigure(0, weight=1)  
    root.grid_rowconfigure(1, weight=0) 
    root.grid_columnconfigure(0, weight=1)

    weather_canvas = WeatherCanvas(root, width=width, height=height)
    weather_canvas.grid(row=0, column=0, sticky="nsew")

    btn_frame = tk.Frame(root)
    btn_frame.grid(row=1, column=0, sticky="we")


    btn_frame.grid_columnconfigure((0,1,2), weight=1)

    def set_clear():
        weather_canvas.set_weather("clear")

    def set_rain():
        weather_canvas.set_weather("rain")

    def set_snow():
        weather_canvas.set_weather("snow")

    btn_clear = tk.Button(btn_frame, text="Ясно", command=set_clear)
    btn_clear.grid(row=0, column=0, sticky="we")

    btn_rain = tk.Button(btn_frame, text="Дощ", command=set_rain)
    btn_rain.grid(row=0, column=1, sticky="we")

    btn_snow = tk.Button(btn_frame, text="Сніг", command=set_snow)
    btn_snow.grid(row=0, column=2, sticky="we")

    root.mainloop()

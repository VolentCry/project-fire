import customtkinter

wind = None
season = None
direction_wind = None
wind_speed = 0
humidity = 0
temperature = 0

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Настройки симуляции")
        self.geometry("1200x650")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("green")

        self.radiobutton_frame = MyRadiobuttonFrame(self, "Направление ветра", values=["Северный ветер", "Южный ветер",
                                                                                       "Западный ветер", "Восточный ветер",
                                                                                       "Северо-Западный ветер", "Юго-Западный ветер",
                                                                                       "Северо-Восточный ветер", "Юго-Восточный ветер"])
        self.radiobutton_frame.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky="nsew")

        self.settings_frame = MySettingsFrame(self, "Дополнительные параметры")
        self.settings_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew")

        self.wind_speed = customtkinter.CTkEntry(self.settings_frame, placeholder_text="Введите скорость ветра")
        self.wind_speed.grid(row=1, column=0, padx=(10, 10), pady=(10, 0), sticky="nwe")
        # self.season_box = customtkinter.CTkOptionMenu(self.settings_frame, values=['Лето', 'Осень', 'Зима', "Весна"])
        # self.season_box.grid(row=4, column=0, padx=(10, 10), pady=(10, 0), sticky="nwe")
        self.label1 = customtkinter.CTkLabel(self.settings_frame, text="м/с", fg_color="gray78", corner_radius=6)
        self.label1.grid(row=1, column=1, padx=(0, 10), pady=(10, 0), sticky="e")
        self.humidity = customtkinter.CTkEntry(self.settings_frame, placeholder_text="Введите относительную влажность воздуха")
        self.humidity.grid(row=2, column=0, padx=(10, 10), pady=(10, 0), sticky="nwe")
        self.label2 = customtkinter.CTkLabel(self.settings_frame, text="%", fg_color="gray78", corner_radius=6)
        self.label2.grid(row=2, column=1, padx=(0, 10), pady=(10, 0), sticky="e")
        self.temp = customtkinter.CTkEntry(self.settings_frame,
                                               placeholder_text="Введите температуру воздуха")
        self.temp.grid(row=3, column=0, padx=(10, 10), pady=(10, 0), sticky="nwe")
        self.label3 = customtkinter.CTkLabel(self.settings_frame, text="C", fg_color="gray78", corner_radius=6)
        self.label3.grid(row=3, column=1, padx=(0, 10), pady=(10, 0), sticky="e")

        self.button = customtkinter.CTkButton(self, text="Запуск симуляции", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def button_callback(self):
        global wind, season, direction_wind, wind_speed, humidity, temperature
        wind = self.radiobutton_frame.get()
        humidity = self.humidity.get()
        # season = self.season_box.get()
        season = "-"
        wind_speed = self.wind_speed.get()
        temperature = self.temp.get()
        app.quit()
        if wind == 'Северный ветер':
            direction_wind = "N"
        elif wind == 'Южный ветер':
            direction_wind = "S"
        elif wind == 'Западный ветер':
            direction_wind = "W"
        elif wind == 'Восточный ветер':
            direction_wind = "E"
        elif wind == 'Северо-Западный ветер':
            direction_wind = "NW"
        elif wind == 'Юго-Западный ветер':
            direction_wind = "SW"
        elif wind == 'Северо-Восточный ветер':
            direction_wind = "NE"
        elif wind == 'Юго-Восточный ветер':
            direction_wind = "SE"


class MyRadiobuttonFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value="")

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray78", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)

class MySettingsFrame(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray78", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

# Запуск программы
app = App()
app.mainloop()

# Запись настроек в отдельный файл
with open("settings.txt", "w") as file:
    file.write(f"{direction_wind}\n{season}\n{wind_speed}\n{humidity}\n{temperature}")
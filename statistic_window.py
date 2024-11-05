import customtkinter, tkinter
"""Скрипт выводящийй окно со статистикой пожара"""

# Значения по умолчанию
air_density = 1.2255 # кг/м3  Обычный стандартная величина плотности воздуха на уровне моря в соответствии
# с Международной стандартной атмосферой
C = 1.005 # кДж/кг * С   Теплоёмкость воздуха.


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Статистика")
        self.geometry("650x850")
        self.grid_columnconfigure((0, 0), weight=1)
        self.grid_rowconfigure(0, weight=1)
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("green")

        self.settings_frame = MySettingsFrame(self)
        self.settings_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # self.title_ = customtkinter.CTkLabel(self, text="Статистика", fg_color="gray78", corner_radius=6)
        # self.title_.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="new")



class MySettingsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0, 1), weight=1)

        self.wind_speed = customtkinter.CTkLabel(self, text="Скорость ветра:")
        self.wind_speed.grid(row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nw")
        self.wind_speed_stat = customtkinter.CTkLabel(self, text="{}", fg_color="gray78", corner_radius=6)
        self.wind_speed_stat.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="ne")

        self.wind_direction = customtkinter.CTkLabel(self, text="Направление ветра:")
        self.wind_direction.grid(row=1, column=0, padx=(10, 10), pady=(10, 0), sticky="nw")
        self.wind_direction_stat = customtkinter.CTkLabel(self, text="{}", fg_color="gray78", corner_radius=6)
        self.wind_direction_stat.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="ne")

        self.temperature = customtkinter.CTkLabel(self, text="Температура воздуха:")
        self.temperature.grid(row=2, column=0, padx=(10, 10), pady=(10, 0), sticky="nw")
        self.temperature_stat = customtkinter.CTkLabel(self, text="{}", fg_color="gray78", corner_radius=6)
        self.temperature_stat.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="ne")

        self.humidity = customtkinter.CTkLabel(self, text="Влажность:")
        self.humidity.grid(row=3, column=0, padx=(10, 10), pady=(10, 0), sticky="nw")
        self.humidity_stat = customtkinter.CTkLabel(self, text="{}", fg_color="gray78", corner_radius=6)
        self.humidity_stat.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="ne")

        self.average_terrain_slope = customtkinter.CTkLabel(self, text="Средний уклон местности:")
        self.average_terrain_slope.grid(row=4, column=0, padx=(10, 10), pady=(10, 0), sticky="nw")
        self.average_terrain_slope_stat = customtkinter.CTkLabel(self, text="{}", fg_color="gray78", corner_radius=6)
        self.average_terrain_slope_stat.grid(row=4, column=1, padx=10, pady=(10, 0), sticky="ne")

        self.air_density = customtkinter.CTkLabel(self, text="Плотность воздуха:")
        self.air_density.grid(row=5, column=0, padx=(10, 10), pady=(10, 0), sticky="nw")
        self.air_density_stat = customtkinter.CTkLabel(self, text=f"{air_density}", fg_color="gray78", corner_radius=6)
        self.air_density_stat.grid(row=5, column=1, padx=10, pady=(10, 0), sticky="ne")

        self.heat_capacity_of_air = customtkinter.CTkLabel(self, text="Удельная теплоёмкость воздуха:")
        self.heat_capacity_of_air.grid(row=6, column=0, padx=(10, 10), pady=(10, 0), sticky="nw")
        self.heat_capacity_of_air_stat = customtkinter.CTkLabel(self, text=f"{C}", fg_color="gray78", corner_radius=6)
        self.heat_capacity_of_air_stat.grid(row=6, column=1, padx=10, pady=(10, 0), sticky="ne")

        self.title_2 = customtkinter.CTkLabel(self, text="Вывод", fg_color="gray78", corner_radius=6)
        self.title_2.grid(row=8, column=0, padx=10, pady=(10, 0), sticky="new", columnspan=2)

        self.formula_Rotermel = customtkinter.CTkLabel(self, text="Скорость огня по формуле Ротермеля:")
        self.formula_Rotermel.grid(row=9, column=0, padx=(10, 10), pady=(10, 0), sticky="nw")
        self.formula_Rotermel_stat = customtkinter.CTkLabel(self, text="{}", fg_color="gray78", corner_radius=6)
        self.formula_Rotermel_stat.grid(row=9, column=1, padx=10, pady=(10, 0), sticky="ne")

        self.title_3 = customtkinter.CTkLabel(self, text="Дополнительная статистика", fg_color="gray78", corner_radius=6)
        self.title_3.grid(row=11, column=0, padx=10, pady=(10, 0), sticky="new", columnspan=2)

def start():
    app = App()
    app.mainloop()

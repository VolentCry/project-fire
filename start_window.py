import time
from fire_programm import simulation
import customtkinter

wind = None
season = None
direction_wind = None
wind_speed = None
humidity = None
temperature = None
incline = None

# Тонкие натсройки
air_density_setting = False
heat_capacity_of_air_setting = False

def out_red(text):
    """Ф-ция цветного вывода текста(красный цвет)"""
    print("\033[31m{}".format(text))

def out_blue(text):
    """Ф-ция цветного вывода текста(синий цвет)"""
    print("\033[34m{}".format(text))

def start_simulation():
    simulation()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Настройки симуляции")
        self.geometry("1200x850")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")
        customtkinter.deactivate_automatic_dpi_awareness()

        self.radiobutton_frame = MyRadiobuttonFrame(self, "Направление ветра", values=["Северный ветер", "Южный ветер",
                                                                                       "Западный ветер", "Восточный ветер",
                                                                                       "Северо-Западный ветер", "Юго-Западный ветер",
                                                                                       "Северо-Восточный ветер", "Юго-Восточный ветер"])
        self.radiobutton_frame.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky="nsew")

        self.radiobutton_frame_plants = MyRadiobuttonFrame(self, "Тип растительности", values=["Низкая трава", "Высокая трава", "Кустарники", "Древесина(трава и подлесок)", "Древесина(подстилка)"])
        self.radiobutton_frame_plants.grid(row=1, column=0, padx=(0, 10), pady=(10, 0), sticky="nsew")

        self.radiobutton_frame_grass = MyRadiobuttonFrame(self, "Количество мёртвых растений",
                                                    values=["Отсутствуют", "Малое", "Среднее", "Большое"])
        self.radiobutton_frame_grass.grid(row=2, column=0, padx=(0, 10), pady=(10, 0), sticky="nsew")

        self.checkbox_frame = MyCheckBoxFrame(self, '"Тонкая" настройка')
        self.checkbox_frame.grid(row=1, column=1, padx=(0, 10), pady=(10, 10), sticky="nsew")

        self.settings_frame = MySettingsFrame(self, "Дополнительные параметры")
        self.settings_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew")

        self.settings_app_frame = MySettingsAppFrame(self, "Настройки окна")
        self.settings_app_frame.grid(row=2, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew")

        self.wind_speed = customtkinter.CTkEntry(self.settings_frame, placeholder_text="Введите скорость ветра")
        self.wind_speed.grid(row=1, column=0, padx=(10, 10), pady=(10, 0), sticky="nwe")
        self.season_box = customtkinter.CTkOptionMenu(self.settings_frame, values=["-", 'Лето', 'Осень', 'Зима', "Весна"])
        self.season_box.grid(row=5, column=0, padx=(10, 10), pady=(10, 0), sticky="nwe", columnspan=2)
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
        self.incline = customtkinter.CTkEntry(self.settings_frame,
                                           placeholder_text="Введите наклон местности")
        self.incline.grid(row=4, column=0, padx=(10, 10), pady=(10, 0), sticky="nwe")
        self.label4 = customtkinter.CTkLabel(self.settings_frame, text="Градусов", fg_color="gray78", corner_radius=6)
        self.label4.grid(row=4, column=1, padx=(0, 10), pady=(10, 0), sticky="e")

        self.button = customtkinter.CTkButton(self, text="Запуск симуляции", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def button_callback(self):
        """Команда выполняемая при нажатии на кнопку 'Запуск симуляции' """
        global wind, season, direction_wind, wind_speed, humidity, temperature, air_density_setting, \
            heat_capacity_of_air_setting, incline

        if self.radiobutton_frame.get() == '':
            out_red("Укажите направление ветра!")
        else:
            if self.humidity.get() == "" or self.wind_speed.get() == "" or self.temp.get() == "" or self.incline.get() == "":
                out_red("ПРЕДУПРЕЖДЕНИЕ! Были указаны не все данные, так что вместо пропусков будут подставлены значения по умолчанию.")
            wind = self.radiobutton_frame.get() # Заносим данные о направлении ветра
            if self.humidity.get() == "": # Сохраняем данные о влажности воздуха
                humidity = 0
            else:
                humidity = self.humidity.get()
            season = self.season_box.get() # Здесь не делаем проверок, так как здесь невозможно не выбрать какой-либо вариант
            if self.wind_speed.get() == "": # Сохраняем данные о скорости ветра
                wind_speed = 0
            else:
                wind_speed = self.wind_speed.get()
            if self.temp.get() == "": # Сохраняем данные о температуре воздуха
                temperature = 0
            else:
                temperature = self.temp.get()
            if self.incline.get() == "": # Сохраняем данные о наклоне местности
                incline = 0
            else:
                incline = self.incline.get()

            # Сохраняем данные о направлении ветра
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

            if self.checkbox_frame.get()[0] == 1:
                air_density_setting = True
            if self.checkbox_frame.get()[1] == 1:
                heat_capacity_of_air_setting = True

            # Проверка на допустимое значение влажности
            if int(humidity) > 100:
                out_red("Влажность не может превышать значение в 100%! Измените параметры и нажмите кнопку запуска симуляции по новой.")
            else:
                # Запись настроек в отдельный файл
                with open("settings.txt", "w") as file:
                    file.write(
                        f"{direction_wind}\n{season}\n{wind_speed}\n{humidity}\n{temperature}\n{air_density_setting}\n"
                        f"{heat_capacity_of_air_setting}\n{incline}")
                file.close()
                app.quit()
                out_blue("Данные успешно сохранены! Сейчас будет запущенны симуляция")
                start_simulation()


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

class MyCheckBoxFrame(customtkinter.CTkFrame):
    """Класс для окошка в котором будут варианты выбора делать ли тонкую настройку расчётов"""
    def __init__(self, master, title):
        super().__init__(master)
        self.state = []
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.checkboxes = []

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray78", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.info = customtkinter.CTkLabel(self, text="*В случаи отказа от выбора тонкой настрйоки в расчётах"
                                                            " будут использоваться значения по умолчанию")
        self.info.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nw")

        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="Точный расчёт плотности воздуха")
        self.checkbox_1.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")
        self.checkbox_2 = customtkinter.CTkCheckBox(self, text="Точный расчёт удельной теплоёмкости")
        self.checkbox_2.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="w")

        self.checkboxes.append(self.checkbox_1)
        self.checkboxes.append(self.checkbox_2)

    def get(self):
        self.state.append(self.checkbox_1.get())
        self.state.append(self.checkbox_2.get())
        return self.state

class MySettingsFrame(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        fg_color = "gray78"

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray78", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=2)


class MySettingsAppFrame(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.grid_columnconfigure([0, 1], weight=1)
        self.title = title

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray78", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew", columnspan=2)
        self.title_theme = customtkinter.CTkLabel(self, text="Тема:", fg_color="gray78", corner_radius=6)
        self.title_theme.grid(row=1, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")
        self.theme_box = customtkinter.CTkOptionMenu(self, values=["Светлая", 'Тёмная', "Системная"])
        self.theme_box.grid(row=1, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew")
        self.button = customtkinter.CTkButton(self, text="Подтвердить изменения", command=self.change_confirm)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def change_confirm(self):
        a = self.theme_box.get()
        # b = self.color_box.get()
        if a == "Тёмная":
            customtkinter.set_appearance_mode("dark")
        elif a == "Светлая":
            customtkinter.set_appearance_mode("light")
        elif a == "Системная":
            customtkinter.set_appearance_mode("system")

# Запуск программы
app = App()
app.mainloop()




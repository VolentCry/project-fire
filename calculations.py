"""Файл со всеми основными расчётами"""
import math

# Основной список данных которые должны будут быть выведены в итог этим файлом
C = 1.005  # Удельная теплоёмкость воздуха

fi = 0  # угол наклона местности (градусы)
I = 0  # интенсивность пожара (кВт/м)
M = 0  # масса сухого вещества на единицу площади (кг/м²)
ro = 0 # плотность воздуха (кг/м³)
flame_temperature = 0 # температура пламени (К)


with open("settings.txt", "r") as file:
    contents = file.readlines()

# Температура воздуха
if len(contents) == 4:
    temperature = None
else:
    temperature = int(contents[4])

humidity = contents[3].replace("\n", "")  # Влажность воздуха (%)
wind_speed = contents[2].replace('\n', '')  # Скорость ветра (м/с)
air_density = bool(contents[5].replace('\n', ''))  # Плотность воздуха
heat_capacity_of_air = bool(contents[6].replace('\n', ''))  # Удельная теплоёмкость воздуха


# Переменные для формулы Ротермеля(Взято из работы Роберта Ротермеля 1972 года "Математическая модель для предсказания распространения пожаров в лесах"
specific_density_of_combustible_material_short = 3.5 # Удельная плотность горючего материала, для НИЗКОЙ травы
specific_density_of_combustible_material_long = 1.5 # Удельная плотность горючего материала, для ВЫСОКОЙ травы
packing_ratio_short = 0.022 # Коэффицент заполнения для НИЗКОЙ травы
packing_ratio_long = 0.034 # Коэффицент заполнения для ВЫСОКОЙ травы
optimal_packing_ratio_short = 1.2655 * (specific_density_of_combustible_material_short ** 0.8189) # Оптимальный коэффициент упаковки для НИЗКОЙ травы
optimal_packing_ratio_long = 1.2655 * (specific_density_of_combustible_material_long ** 0.8189) # Оптимальный коэффициент упаковки для ВЫСОКОЙ травы
A_short = (5.371 * (specific_density_of_combustible_material_short ** 0.1) - 7.27) ** -1 # Неизвестный коэффициент для НИЗКОЙ травы
A_long = (5.371 * (specific_density_of_combustible_material_long ** 0.1) - 7.27) ** -1 # Неизвестный коэффициент для ВЫСОКОЙ травы
C_short = 7.47 * math.exp(-0.133 * (specific_density_of_combustible_material_short ** 0.55)) # Неизвестный коэффициент для НИЗКОЙ травы
C_long = 7.47 * math.exp(-0.133 * (specific_density_of_combustible_material_long ** 0.55)) # Неизвестный коэффициент для ВЫСОКОЙ травы
E_short = 0.715 * math.exp(-3.59 * (10 ** -4) * specific_density_of_combustible_material_short) # Неизвестный коэффициент для НИЗКОЙ травы
E_long = 0.715 * math.exp(-3.59 * (10 ** -4) * specific_density_of_combustible_material_long) # Неизвестный коэффициент для ВЫСОКОЙ травы
B_short = 0.02526 * (specific_density_of_combustible_material_short ** 0.54) # Неизвестный коэффициент для НИЗКОЙ травы
B_long = 0.02526 * (specific_density_of_combustible_material_long ** 0.54) # Неизвестный коэффициент для ВЫСОКОЙ травы
potential_reaction_rate_short = ((specific_density_of_combustible_material_short ** 1.5)/(83.301+0.01 * (specific_density_of_combustible_material_short ** 1.5))) * \
                                ((packing_ratio_short / optimal_packing_ratio_short) ** A_short) * math.exp(A_short * (1 - packing_ratio_short / optimal_packing_ratio_short)) # Потенциальная скорость реакции для НИЗКОЙ травы
potential_reaction_rate_long = ((specific_density_of_combustible_material_long ** 1.5)/(83.301+0.01 * (specific_density_of_combustible_material_long ** 1.5))) * \
                                ((packing_ratio_long / optimal_packing_ratio_long) ** A_long) * math.exp(A_long * (1 - packing_ratio_long / optimal_packing_ratio_long)) # Потенциальная скорость реакции для ВЫСОКОЙ травы
heating_efficiency_coefficient_of_combustible_material_short = math.exp(-425.75/specific_density_of_combustible_material_short) # Коэффицент эффективности нагревания горючего материала для НИЗКОЙ травы
heating_efficiency_coefficient_of_combustible_material_long = math.exp(-425.75/specific_density_of_combustible_material_long) # Коэффицент эффективности нагревания горючего материала для ВЫСОКОЙ травы
the_coefficient_determined_by_combustible_materials_short = ((192 + 0.8514 * specific_density_of_combustible_material_short) ** -1) * \
                                                            math.exp((0.792 + 2.234 * (specific_density_of_combustible_material_short ** 0.37)) * (packing_ratio_short + 0.1)) # Коэффициент определяемый горючими материалами для НИЗКОЙ травы
the_coefficient_determined_by_combustible_materials_long = ((192 + 0.8514 * specific_density_of_combustible_material_long) ** -1) * \
                                                            math.exp((0.792 + 2.234 * (specific_density_of_combustible_material_long ** 0.37)) * (packing_ratio_long + 0.1)) # Коэффициент определяемый горючими материалами для ВЫСОКОЙ травы
wind_coefficient_short = C_short * (wind_speed ** B_short) * (packing_ratio_short / optimal_packing_ratio_short) ** E_short # Ветрянной коэффициент для НИЗКОЙ травы
wind_coefficient_long = C_long * (wind_speed ** B_long) * (packing_ratio_long / optimal_packing_ratio_long) ** E_long # Ветрянной коэффициент для ВЫСОКОЙ травы
fuel_supply_short = 0.034 # Запас горючего материала для НИЗКОЙ травы
fuel_supply_long = 0.138 # Запас горючего материала для ВЫСОКОЙ травы

fire_speed_formula_Rotermel = 0  # Скорость распространения пламени по формуле Ротермеля





def accurate_calculations():
    """Основной алгоритм рассчётов"""
    global C, fire_speed_formula_Rotermel, I, M, fi, ro, flame_temperature, temperature
    # Рассчёт удельной теплоёмкости воздуха
    if heat_capacity_of_air:
        if temperature >= 20:
            C_up_20 = 1.005 - 0.0000047 * temperature  # Расчёт удельной теплоёмкости воздуха при температуре ВЫШЕ 20-ти градусов
            C = C_up_20
        else:
            C_low_20 = 1.008 - 0.0000033 * temperature  # Расчёт удельной теплоёмкости воздуха при температуре НИЖЕ 20-ти градусов
            C = C_low_20

    # Рассчёт плотности воздуха

    # Рассчёт скорости распространения пламени по формуле Ротермеля
    fire_speed_formula_Rotermel = 0


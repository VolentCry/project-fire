"""
Описание проекта:
Это программа, которая на основе клеточных автоматов будет симулировать реальную географическую местность и
распространение огня на ней в зависимоти от разных условий

Список задач:
1. Генерация леса +
2. Распространение огня +
3. Имитация водных преград +
4. Создание рельефа на модели
5. Имитация ветра +
6. Построение реального ландшафта по топографической карте
7. Отображение посёлков и городов

Используемые патерны и их назначение:
1. Правило B35678/S5678 - Диамёба - Генерация леса
2. Правило B4678/S35678 - Отжиг - Имитация огня

Разновидности состояния клеток:
0 - Трава
1 - Дерево
2 - Огонь
3 - Вода
4 - Земля
"""

import random
import time
import asyncio
import math
import pygame
import numpy as np


# Направление ветра
"""Виды ветра и их запись:
None - отсустствие ветра
N - северный ветер
S - южный ветер
W - западный ветер
E - восточный ветер
NE - северо-восточный
SE - юго-восточный
SW - южно-западный
NW - северо-восточный

Влажность:
если ниже 30, то не влияет на скорость
есди от 30 и до 70 замедляет скорость
если от 70 и до 100, то очень замедляет скорость

Скорость ветра:


Температура:
если до 15 градусов - не влияет
от 15 и до 25 - увеличивает немного скорость
выше 25 - сильно увеличивает скорость

"""

with open("settings.txt", "r") as file:
    contents = file.readlines()

direction_of_the_wind = contents[0].replace('\n', '')
season = contents[1].replace("\n", "")
if len(contents) == 4:
    temperature = None
else:
    temperature = contents[4]
humidity = contents[3].replace("\n", "")
wind_speed = contents[2].replace('\n', '')
if direction_of_the_wind is None:
    direction_of_the_wind = None
if season is None:
    season = None
if temperature is None:
    temperature = None
if humidity is None:
    humidity = None
if int(humidity) > 100:
    raise ValueError("Влажность воздуха не может превыщать 100 процентов")
if wind_speed is None:
    wind_speed = None


def generate_coordinates(min_distance: int, field_size: int, num_points: int):
    """Генератор рандомных координат
    На вход принимает три значения: минимальная дистанция между координатами; размер поля в формате N x N;
    количество пар координат которое вам нужны"""
    points = []
    while len(points) < num_points:
        new_point = [random.randint(0, field_size), random.randint(0, field_size)]
        if all(math.sqrt((p[0] - new_point[0]) ** 2 + (p[1] - new_point[1]) ** 2) >= min_distance for p in points):
            points.append(new_point)
    return points

# Создаём список точек возгарания для дальнейшего расчёта скорости движения огня
flashpoints = []

# Выборка рандомных координат
coordinates = generate_coordinates(8, 99, 7)  # лес
coordinates_lakes = generate_coordinates(5, 99, 15)  # озёра

# Размеры окна
WIDTH, HEIGHT = 1000, 1000

# Размеры сетки
ROWS, COLS = 100, 100

# Размер каждой клетки
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS

# Название окна
pygame.display.set_caption("Имитация лесных пожаров. Поколение: 0")

# Инициализация Pygame
pygame.init()

# Инициализация сетки
grid = np.zeros((ROWS, COLS))

def update_grid_forest_building():
    """Обновление сетки(построение леса) по принципу правила 'Диамёба'"""
    global grid
    new_grid = grid.copy()
    for i in range(ROWS):
        for j in range(COLS):
            state = grid[i][j]
            neighbours_list = get_neighbours_mode(i, j)
            if state == 0 and (neighbours_list[1] == 3 or 5 <= neighbours_list[1] <= 8):  # Праивло рождения
                new_grid[i][j] = 1
            elif state == 1 and (1 <= neighbours_list[1] <= 2 or neighbours_list[1] == 4):  # Правило смерти
                new_grid[i][j] = 0
    grid = new_grid

def update_grid_lakes_building():
    """Обновление сетки(построение озёр) по принципу правила 'Диамёба'"""
    global grid
    new_grid = grid.copy()
    for i in range(ROWS):
        for j in range(COLS):
            state = grid[i][j]
            neighbours_list = get_neighbours_mode(i, j)
            if state == 0 and (neighbours_list[3] == 3 or 5 <= neighbours_list[3] <= 8):  # Праивло рождения
                new_grid[i][j] = 3
            elif state == 3 and (1 <= neighbours_list[3] <= 2 or neighbours_list[3] == 4):  # Правило смерти
                new_grid[i][j] = 0
    grid = new_grid

def update_grid_fire():
    """Обновление сетки(взаимодействие огня с деревом, и с водой, и зависимость от ветра)
    - ПРАВИЛО ПОВЕДЕНИЯ ОГНЯ -
    """
    global grid
    global direction_of_the_wind
    new_grid = grid.copy()
    for i in range(ROWS):
        for j in range(COLS):
            state = grid[i][j]
            neighbours_list = get_neighbours_mode(i, j)

            """Задаём функции движения огня в разные стороны по лесной местности и траве"""
            def fire_down(x, y):
                # распролстранение огня на клетку вниз
                if x >= 99:
                    pass
                else:
                    if grid[x + 1][y] == 1: # Дерево
                        new_grid[x + 1][y] = 2
                    elif grid[x + 1][y] == 0: # Трава
                        new_grid[x + 1][y] = 2
                    elif grid[x + 1][y] == 3: # Вода
                        new_grid[x][y] = 4

            def fire_right(x, y):
                # распролстранение огня на клетку вправо
                if y >= 99:
                    pass
                else:
                    if new_grid[x][y + 1] == 1: # Дерево
                        new_grid[x][y + 1] = 2
                    elif new_grid[x][y + 1] == 0: # Трава
                        new_grid[x][y + 1] = 2
                    elif new_grid[x][y + 1] == 3: # Вода
                        new_grid[x][y] = 4

            def fire_up(x, y):
                # распролстранение огня на клетку вверх
                if new_grid[x - 1][y] == 1 and x - 1 >= 0: # Дерево
                    new_grid[x - 1][y] = 2
                elif new_grid[x - 1][y] == 2 and x - 1 >= 0: # Трава
                    new_grid[x - 1][y] = 2
                elif new_grid[x - 1][y] == 3 and x - 1 >= 0: # Вода
                    new_grid[x][y] = 4

            def fire_left(x, y):
                # распролстранение огня на клетку влево
                if new_grid[x][y - 1] == 1 and y - 1 >= 0: # Дерево
                    new_grid[x][y - 1] = 2
                if new_grid[x][y - 1] == 0 and y - 1 >= 0: # Трава
                    new_grid[x][y - 1] = 2
                elif new_grid[x][y - 1] == 3 and y - 1 >= 0: # Вода
                    new_grid[x][y] = 4

            def diagonal_left_up(x, y):
                # распролстранение огня влево вверх по диагонали
                if y - 1 < 0 or x - 1 < 0 or y == 0 or x == 0:
                    pass
                elif new_grid[x - 1][y - 1] == 1: # Дерево
                    new_grid[x - 1][y - 1] = 2
                elif new_grid[x - 1][y - 1] == 0: # Трава
                    new_grid[x - 1][y - 1] = 2
                elif new_grid[x - 1][y - 1] == 3 and y - 1 >= 0 and x - 1 >= 0: # Вода
                    new_grid[x][y] = 4

            def diagonal_right_up(x, y):
                # распролстранение огня вправо вверх по диагонали
                if x - 1 < 0 or y + 1 > 99 or x == 0 or y == 99:
                    pass
                elif new_grid[x - 1][y + 1] == 1 and x - 1 >= 0 and y + 1 <= 99: # Дерево
                    new_grid[x - 1][y + 1] = 2
                elif new_grid[x - 1][y + 1] == 0 and x - 1 >= 0 and y + 1 <= 99: # Трава
                    new_grid[x - 1][y + 1] = 2
                elif new_grid[x - 1][y + 1] == 3 and y + 1 > 99 and x - 1 >= 0: # Вода
                    new_grid[x][y] = 4

            def diagonal_left_down(x, y):
                # распролстранение огня влево вниз по диагонали
                if y - 1 < 0 or x + 1 > 99 or y == 0 or x == 99:
                    pass
                elif new_grid[x + 1][y - 1] == 1 and y - 1 >= 0 and x + 1 <= 99: # Дерево
                    new_grid[x + 1][y - 1] = 2
                elif new_grid[x + 1][y - 1] == 0 and y - 1 >= 0 and x + 1 <= 99: # Трава
                    new_grid[x + 1][y - 1] = 2
                elif new_grid[x + 1][y - 1] == 3 and y - 1 >= 0 and x + 1 > 0: # Вода
                    new_grid[x][y] = 4

            def diagonal_right_down(x, y):
                # распролстранение огня вправо вниз по диагонали
                if y + 1 > 99 or x + 1 > 99 or x == 99 or y == 99:
                    pass
                elif new_grid[x + 1][y + 1] == 1 and y + 1 <= 99 and x + 1 <= 99: # Дерево
                    new_grid[x + 1][y + 1] = 2
                elif new_grid[x + 1][y + 1] == 0 and y + 1 <= 99 and x + 1 <= 99: # Трава
                    new_grid[x + 1][y + 1] = 2
                elif new_grid[x + 1][y + 1] == 3 and y + 1 >= 99 and x + 1 >= 99:
                    new_grid[x][y] = 4

            if state == 2 and (neighbours_list[1] >= 1 or neighbours_list[0] >= 1):  # Заменяет клетку дерева, на которую попал огонь на клетку земли
                new_grid[i][j] = 4  # задаём новый статус клетки, то есть клетку огня меняем на землю
                """По идеи дальеш проевряем все клетку вокруг, чтоб, елси она окажется деревом,
                то тоже заменить её на огонь, по идеи, нужно сделать некий рандом, то есть чтобы распространение
                огня по деревья не было равномерным(это некрасиво выглядит), поэтому нужно добавить некие задаржки,
                роандомайзер, типо такого, метами возможно затухание огня с небольшим шансом, чтобы добапвить
                картинки реалистичности"""

                # time.sleep(0.00002)

                if direction_of_the_wind == "N":  # Северный ветер
                    def rule_wind_N1(x, y):
                        """Движение огня при северном ветре 1"""
                        north_direction_plus = [fire_up, diagonal_left_up, diagonal_right_up, fire_left, fire_right]
                        get_random = random.sample(north_direction_plus, 3)
                        return get_random[0](x, y), get_random[1](x, y), get_random[2](x, y)

                    def rule_wind_N2(x, y):
                        """Движение огня при северном ветре 2"""
                        other_func = [fire_down, diagonal_left_down, diagonal_right_down, fire_left, fire_right]
                        get_random = random.sample(other_func, 3)
                        return get_random[0](x, y), get_random[1](x, y)

                    rule_wind_N1(i, j)
                    if random.randint(1, 100) <= 25:
                        rule_wind_N2(i, j)

                elif direction_of_the_wind == "S":  # Южный ветер

                    def rule_wind_S1(x, y):
                        """Движение огня при южном ветре 1"""
                        north_direction_plus = [fire_down, diagonal_left_down, diagonal_right_down, fire_left,
                                                fire_right]
                        get_random = random.sample(north_direction_plus, 3)
                        return get_random[0](x, y), get_random[1](x, y), get_random[2](x, y)

                    def rule_wind_S2(x, y):
                        """Движение огня при южном ветре 2"""
                        other_func = [fire_up, diagonal_left_up, diagonal_right_up, fire_left, fire_right]
                        get_random = random.sample(other_func, 3)
                        return get_random[0](x, y), get_random[1](x, y)

                    rule_wind_S1(i, j)
                    if random.randint(1, 100) <= 25:
                        rule_wind_S2(i, j)

                elif direction_of_the_wind == "W":  # Западный ветер

                    def rule_wind_W1(x, y):
                        """Движение огня при западном ветре 1"""
                        north_direction_plus = [fire_left, diagonal_left_down, diagonal_left_up, fire_up, fire_down]
                        get_random = random.sample(north_direction_plus, 3)
                        return get_random[0](x, y), get_random[1](x, y), get_random[2](x, y)

                    def rule_wind_W2(x, y):
                        """Движение огня при западном ветре 2"""
                        other_func = [fire_up, diagonal_right_down, diagonal_right_up, fire_left, fire_down]
                        get_random = random.sample(other_func, 3)
                        return get_random[0](x, y), get_random[1](x, y)

                    rule_wind_W1(i, j)
                    if random.randint(1, 100) <= 25:
                        rule_wind_W2(i, j)

                elif direction_of_the_wind == "E":  # Восточный ветер

                    def rule_wind_E1(x, y):
                        """Движение огня при восточном ветре 1"""
                        north_direction_plus = [fire_down, diagonal_right_up, diagonal_right_down, fire_up, fire_right]
                        get_random = random.sample(north_direction_plus, 3)
                        return get_random[0](x, y), get_random[1](x, y), get_random[2](x, y)

                    def rule_wind_E2(x, y):
                        """Движение огня при восточном ветре 2"""
                        other_func = [fire_up, diagonal_left_up, diagonal_left_down, fire_left, fire_down]
                        get_random = random.sample(other_func, 3)
                        return get_random[0](x, y), get_random[1](x, y)

                    rule_wind_E1(i, j)
                    if random.randint(1, 100) <= 25:
                        rule_wind_E2(i, j)

                elif direction_of_the_wind == "NE":  # Северо-восточный ветер

                    def rule_wind_NE1(x, y):
                        """Движение огня при северо-восточном ветре 1"""
                        north_direction_plus = [diagonal_right_up, fire_up, fire_right]
                        get_random = random.sample(north_direction_plus, 1)
                        return get_random[0](x, y)

                    def rule_wind_NE2(x, y):
                        """Движение огня при северо-восточном ветре 2"""
                        other_func = [diagonal_right_up, fire_up, fire_right, diagonal_left_up, diagonal_right_down]
                        get_random = random.sample(other_func, 3)
                        return get_random[0](x, y), get_random[1](x, y), get_random[2](x, y)

                    def rule_wind_NE3(x, y):
                        """Движение огня при северо-восточном ветре 3"""
                        other_func = [diagonal_left_down, fire_left, fire_down]
                        get_random = random.sample(other_func, 2)
                        return get_random[0](x, y), get_random[1](x, y)

                    rule_wind_NE1(i, j)
                    if random.randint(1, 100) <= 40:
                        rule_wind_NE2(i, j)
                    if random.randint(1, 100) <= 28:
                        rule_wind_NE3(i, j)

                elif direction_of_the_wind == "SE":  # Юго-восточный

                    def rule_wind_SE1(x, y):
                        """Движение огня при юго-восточном ветре 1"""
                        north_direction_plus = [diagonal_right_down, fire_down, fire_right]
                        get_random = random.sample(north_direction_plus, 1)
                        return get_random[0](x, y)

                    def rule_wind_SE2(x, y):
                        """Движение огня при юго-восточном ветре 2"""
                        other_func = [diagonal_right_down, fire_down, fire_right, diagonal_left_down, diagonal_right_up]
                        get_random = random.sample(other_func, 3)
                        return get_random[0](x, y), get_random[1](x, y), get_random[2](x, y)

                    def rule_wind_SE3(x, y):
                        """Движение огня при юго-восточном ветре 3"""
                        other_func = [diagonal_right_up, fire_left, fire_up]
                        get_random = random.sample(other_func, 2)
                        return get_random[0](x, y), get_random[1](x, y)

                    rule_wind_SE1(i, j)
                    if random.randint(1, 100) <= 40:
                        rule_wind_SE2(i, j)
                    if random.randint(1, 100) <= 28:
                        rule_wind_SE3(i, j)

                elif direction_of_the_wind == "SW":  # Юго-западный

                    def rule_wind_SW1(x, y):
                        """Движение огня при юго-западном ветре 1"""
                        north_direction_plus = [diagonal_left_down, fire_down, fire_left]
                        get_random = random.sample(north_direction_plus, 1)
                        return get_random[0](x, y)

                    def rule_wind_SW2(x, y):
                        """Движение огня при юго-западном ветре 2"""
                        other_func = [diagonal_left_up, fire_down, diagonal_left_down, fire_down, diagonal_right_down]
                        get_random = random.sample(other_func, 3)
                        return get_random[0](x, y), get_random[1](x, y), get_random[2](x, y)

                    def rule_wind_SW3(x, y):
                        """Движение огня при юго-западном ветре 3"""
                        other_func = [diagonal_right_up, fire_right, fire_up]
                        get_random = random.sample(other_func, 2)
                        return get_random[0](x, y), get_random[1](x, y)

                    rule_wind_SW1(i, j)
                    if random.randint(1, 100) <= 40:
                        rule_wind_SW2(i, j)
                    if random.randint(1, 100) <= 28:
                        rule_wind_SW3(i, j)

                elif direction_of_the_wind == "NW":  # Северо-западный

                    def rule_wind_NW1(x, y):
                        """Движение огня при юго-восточном ветре 1"""
                        north_direction_plus = [diagonal_left_up, fire_up, fire_left]
                        get_random = random.sample(north_direction_plus, 1)
                        return get_random[0](x, y)

                    def rule_wind_NW2(x, y):
                        """Движение огня при юго-восточном ветре 2"""
                        other_func = [diagonal_left_up, fire_up, fire_left, diagonal_right_up, diagonal_left_down]
                        get_random = random.sample(other_func, 3)
                        return get_random[0](x, y), get_random[1](x, y), get_random[2](x, y)

                    def rule_wind_NW3(x, y):
                        """Движение огня при юго-восточном ветре 3"""
                        other_func = [diagonal_right_down, fire_right, fire_down]
                        get_random = random.sample(other_func, 2)
                        return get_random[0](x, y), get_random[1](x, y)

                    rule_wind_NW1(i, j)
                    if random.randint(1, 100) <= 40:
                        rule_wind_NW2(i, j)
                    if random.randint(1, 100) <= 28:
                        rule_wind_NW3(i, j)

                else:  # Ситуация если ветра нет
                    def rule_no_wind(x, y):
                        """Движение огня при отсутствии ветра"""
                        all_func = [fire_down, fire_up, fire_left, fire_right, diagonal_left_down, diagonal_right_down,
                                    diagonal_left_up, diagonal_right_up]
                        get_random = random.sample(all_func, 3)
                        return get_random[0](x, y), get_random[1](x, y), get_random[2](x, y)

                    rule_no_wind(i, j)

            elif state == 2 and neighbours_list[0] + neighbours_list[2] + neighbours_list[4] == 8:  # Устраняет клетки огня, стоящие посреди
                # клеток травы/деревьев
                new_grid[i][j] = 4
            elif state == 2 and neighbours_list[4] + neighbours_list[2] == 8:  # Устраняет клетки огня, стоящие посреди
                # клеток земли
                new_grid[i][j] = 4
            elif state == 2 and neighbours_list[3] >= 1:  # Устраняет клетки огня, стоящие рядом с клеткой воды
                new_grid[i][j] = 4
    grid = new_grid


def get_neighbours_mode(x, y):
    """Помимо того, что эта функция видёт подсчёт количества соседей клетки, так она считает конкретко количесвто
     клеток каждого типа (от 0 и до 3)"""
    neighbours = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            x_edge = (x + i + ROWS) % ROWS
            y_edge = (y + j + COLS) % COLS
            cell_value = grid[x_edge][y_edge]
            neighbours[cell_value] += 1
    return neighbours


def simulation():
    """Основаная функция"""
    clock = pygame.time.Clock()
    run = True
    simulate = False
    generation_counter = 0  # Счётчик поколений
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    def draw_grid():
        """Отрисовка сетки, задаём все значения, их цвета и что они будут обозначать в клеточном автомате"""
        for p in range(ROWS):
            for q in range(COLS):
                rect = pygame.Rect(q * CELL_WIDTH, p * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                if grid[p][q] == 4:
                    # Отрисовка земли
                    pygame.draw.rect(WIN, (153, 102, 51), rect)
                elif grid[p][q] == 1:
                    # Отрисовка дерева
                    pygame.draw.rect(WIN, (93, 161, 92), rect)
                elif grid[p][q] == 2:
                    # Отрисовка огня
                    pygame.draw.rect(WIN, (238, 129, 20), rect)
                elif grid[p][q] == 3:
                    # Отрисовка воды
                    pygame.draw.rect(WIN, (51, 153, 255), rect)
                elif grid[p][q] == 0:
                    # Отрисовка травы
                    pygame.draw.rect(WIN, (105, 196, 111), rect)
                    pass

    # генератор леса(генерирует 7 основных точек от куда будет формироваться лес)
    for j, i in coordinates:
        grid[j][i] = 1
        if i + 1 > 99:
            pass
        else:
            grid[j][i + 1] = 1
        if j + 1 > 99:
            pass
        else:
            grid[j + 1][i - 1] = 1
        if j + 1 > 99:
            pass
        else:
            grid[j + 1][i] = 1
        if j + 1 > 99:
            pass
        elif i + 1 > 99:
            pass
        elif i + 1 > 99 and j + 1 > 99:
            pass
        else:
            grid[j + 1][i + 1] = 1
        if j + 1 > 99:
            pass
        elif i + 2 > 99:
            pass
        elif i + 2 > 99 and j + 1 > 99:
            pass
        else:
            grid[j + 1][i + 2] = 1
        if j + 1 > 99:
            pass
        elif i + 3 > 99:
            pass
        elif i + 3 > 99 and j + 1 > 99:
            pass
        else:
            grid[j + 1][i + 3] = 1
        if j + 2 > 99:
            pass
        else:
            grid[j + 2][i - 2] = 1
        if j + 2 > 99:
            pass
        else:
            grid[j + 2][i - 1] = 1
        if j + 2 > 99:
            pass
        else:
            grid[j + 2][i] = 1
        if j + 2 > 99:
            pass
        elif i + 1 > 99:
            pass
        elif i + 1 > 99 and j + 2 > 99:
            pass
        else:
            grid[j + 2][i + 1] = 1
        if j + 2 > 99:
            pass
        elif i + 2 > 99:
            pass
        elif i + 2 > 99 and j + 2 > 99:
            pass
        else:
            grid[j + 2][i + 2] = 1
        if j + 2 > 99:
            pass
        elif i + 3 > 99:
            pass
        elif i + 3 > 99 and j + 2 > 99:
            pass
        else:
            grid[j + 2][i + 3] = 1
        if j + 3 > 99:
            pass
        else:
            grid[j + 3][i - 2] = 1
        if j + 3 > 99:
            pass
        else:
            grid[j + 3][i - 1] = 1
        if j + 3 > 99:
            pass
        else:
            grid[j + 3][i] = 1
        if j + 4 > 99:
            pass
        else:
            grid[j + 4][i - 2] = 1
        if j + 4 > 99:
            pass
        else:
            grid[j + 4][i - 1] = 1

    # Эта штука генерирует лес, а потом уже отображает кратинку, но из-за этого конечно складывается ощущение
    # не рабочей программы, не знаю как это пофиксить
    for i in range(0, 100):
        update_grid_forest_building()

    # Генерация озёр
    for i, j in coordinates_lakes:
        state = grid[i][j]
        neighbours_list = get_neighbours_mode(i, j)
        if (i + 3) < 98 and (j + 3) < 98 and (i - 3) >= 0 and (j - 3) >= 0:
            """Здесь мы короче генерируем озёра точно таким же образом как и лес"""
            if (state == 0 and neighbours_list[0] == 8) and (
                    grid[i - 3][j - 3] == 0 and get_neighbours_mode(i - 3, j - 3)[0] == 8) \
                    and (grid[i][j - 3] == 0 and get_neighbours_mode(i, j - 3)[0] == 8) and (
                    grid[i + 3][j - 3] == 0 and get_neighbours_mode(i + 3, j - 3)[0] == 8) \
                    and (grid[i - 3][j] == 0 and get_neighbours_mode(i - 3, j)[0] == 8) and (
                    grid[i + 3][j] == 0 and get_neighbours_mode(i + 3, j)[0] == 8) \
                    and (grid[i - 3][j + 3] == 0 and get_neighbours_mode(i - 3, j + 3)[0] == 8) \
                    and (grid[i][j + 3] == 0 and get_neighbours_mode(i, j + 3)[0] == 8) \
                    and (grid[i + 3][j + 3] == 0 and get_neighbours_mode(i + 3, j + 3)[0] == 8):

                grid[i][j] = 3
                grid[i - 1][j + 3] = 3
                grid[i][j + 2] = 3
                grid[i][j + 3] = 3
                grid[i - 1][j + 2] = 3
                grid[i][j + 1] = 3
                grid[i - 1][j + 1] = 3
                grid[i - 2][j + 1] = 3
                grid[i + 2][j - 1] = 3
                grid[i + 2][j - 2] = 3
                grid[i + 1][j - 2] = 3
                grid[i + 1][j - 1] = 3
                grid[i + 1][j] = 3
                grid[i - 1][j - 1] = 3
                grid[i][j - 1] = 3
                grid[i][j - 2] = 3
                grid[i - 1][j] = 3
                grid[i - 2][j] = 3

    # Эта штука генерирует озёра, а потом уже отображает кратинку
    for i in range(0, 10):
        update_grid_lakes_building()

    # Основной цикл программы
    while run:
        clock.tick(10)  # Настройка скорости смены поколений
        draw_grid()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Запуск основного алгоритма
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Нарисовать "Огонь"
                x, y = pygame.mouse.get_pos()
                grid[y // CELL_HEIGHT][x // CELL_WIDTH] = 2
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Запуск/Остановка симуляции
                    simulate = not simulate
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    # Смена одного поколения
                    update_grid_fire()
                    pygame.display.set_caption(f"Итмитация лесных пожаров. поколение: {generation_counter}")
                    generation_counter += 1
                elif event.key == pygame.K_c:
                    # Очистка поля
                    grid.fill(0)
        if simulate:
            update_grid_fire()
            pygame.display.set_caption(f"Итмитация лесных пожаров. поколение: {generation_counter}")
            generation_counter += 1
    pygame.quit()
    print(f"Итоговое количество поколений: {generation_counter}")  # Вывод количества поколений

simulation()


print("Итоговый расчёт скорости ветра")
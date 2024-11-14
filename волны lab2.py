import pygame
import math
import random
import json

pygame.init()

# На данном этапе я настраиваю окно
win_width, win_height = 800, 600
screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Симуляция волн")

# Выбираю цвета
bg_color = (240, 230, 240)  # белый
wave_col = (0, 250, 0)      # зеленый
float_col = (240, 120, 240)  # фиолетовый

# Загружаю начальные данные из JSON
json_file = "waves.json"
with open(json_file) as f:
    json_data = json.load(f)

# Инициализацирую данные
wave_count = json_data["number of waves"]  # Количество волн
wave_attributes = json_data["waves"]        # Параметры волн
float_radius = json_data["poplavok radius"] # Радиус поплавка

# Расположение поплавков
float_positions = [win_height // (wave_count + 1) * (i + 1) for i in range(wave_count)]

# Вес поплавков
float_weights = [random.uniform(0.5, 2.0) for _ in range(wave_count)]  # Случайные веса для каждого поплавка

running = True
clock = pygame.time.Clock()

while running:
    # Заливка фона
    screen.fill(bg_color)

    # Обработка выхода из программы
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление волн и поплавков
    elapsed_time = pygame.time.get_ticks() / 1000  # Время в секундах
    for i, wave in enumerate(wave_attributes):
        amplitude = wave["amplitude"]  # Амплитуда волны
        period = wave["period"]         # Период волны
        speed = wave["speed"]           # Скорость волны

        # Отрисовка волны
        wave_y = float_positions[i]  # Вертикальная позиция волны
        for x in range(win_width):
            y = wave_y + amplitude * math.sin(2 * math.pi * (x / period) - speed * elapsed_time)
            pygame.draw.circle(screen, wave_col, (x, int(y)), 1)

        # Расчет позиции поплавка с учетом веса
        float_x = (elapsed_time * 100) % win_width  # Положение поплавка по оси X
        wave_effect_y = wave_y + amplitude * math.sin(2 * math.pi * (float_x / period) - speed * elapsed_time)

        # Корректировка позиции поплавка в зависимости от веса: более тяжелые поплавки тонут
        float_y = wave_effect_y + float_weights[i] * 5  # Визуализация эффекта веса

        # Отрисовка поплавка
        pygame.draw.circle(screen, float_col, (int(float_x), int(float_y)), float_radius)

    pygame.display.update()  # Обновление экрана
    clock.tick(150)          # Ограничение частоты кадров

pygame.quit()

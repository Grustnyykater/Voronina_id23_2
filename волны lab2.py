import pygame
import math
import random
import json

pygame.init()

# настройка окна
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Волны")

# определение цветов
background_color = (240, 230, 240)
wave_color = (0, 250, 0)
poplavok_color = (240, 120, 240)

# загрузка начальных данных из JSON
data_file = "waves.json"
with open(data_file) as file:
    data = json.load(file)

# инициализация данных
num_waves = data["number of waves"]
wave_parametry = data["waves"]
poplavok_radius = data["poplavok radius"]

# позиции поплавков
poplavok_positions = [height // (num_waves + 1) * (i + 1) for i in range(num_waves)]

# вес поплавка
poplavok_weights = [random.uniform(0.5, 2.0) for _ in range(num_waves)]  # случайные веса для каждого поплавка

running = True
clock = pygame.time.Clock()

while running:
    # заливка фона
    window.fill(background_color)

    # обработка выхода
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # обновление волн и поплавков
    time = pygame.time.get_ticks() / 1000  # время в секундах
    for i, wave in enumerate(wave_parametry):
        amplitude = wave["amplitude"]
        period = wave["period"]
        speed = wave["speed"]

        # отрисовка волны
        wave_y = poplavok_positions[i]
        for x in range(width):
            y = wave_y + amplitude * math.sin(2 * math.pi * (x / period) - speed * time)
            pygame.draw.circle(window, wave_color, (x, int(y)), 1)

        # расчет позиции поплавка с учетом веса
        poplavok_x = (time * 100) % width
        wave_effect_y = wave_y + amplitude * math.sin(2 * math.pi * (poplavok_x / period) - speed * time)

        # учитываем вес: чем больше вес, тем меньше колебаний поплавка
        poplavok_y = wave_effect_y + poplavok_weights[i] * 5  # визуализации эффекта веса

        # отрисовка поплавка
        pygame.draw.circle(window, poplavok_color, (int(poplavok_x), int(poplavok_y)), poplavok_radius)

    pygame.display.update()
    clock.tick(150)

pygame.quit()

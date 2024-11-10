from tkinter import *
from math import *

# Главное окно
window = Tk()
size = 600
canvas = Canvas(window, width=size, height=size)  # Установка размеров
canvas.pack()

radius = 200
center = 300, 300

# Рисуем окружность
canvas.create_oval(center[0] - radius, center[1] - radius,
                   center[0] + radius, center[1] + radius)

angle = 0
speed = 10
direction = 1  # Изменил на 1, чтобы точка двигалась по часовой стрелке

def move():
    global angle
    r_angle = radians(angle)  # Конвертируем угол в радианы
    # Вычисление координат точки на окружности
    point_x = center[0] + radius * cos(r_angle)
    point_y = center[1] + radius * sin(r_angle)
    canvas.delete("point")  # Удаляем предыдущую точку
    # Рисуем точку
    canvas.create_oval(point_x - 5, point_y - 5, point_x + 5, point_y + 5, fill="pink", tag="point")
    angle += direction * speed  # Увеличиваем угол для создания движения точки
    if angle >= 360:  # Убеждаемся, что угол остается в пределах 0-360
        angle -= 360
    window.after(60, move)

# Запускаем анимацию
move()
window.mainloop()
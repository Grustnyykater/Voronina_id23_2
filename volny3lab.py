import pygame
import math
import random
import json

pygame.init()

# настраиваю окно
shirina, dlina = 800, 600
screen = pygame.display.set_mode((shirina, dlina))
pygame.display.set_caption("Симуляция волн")

# настраиваю цвета
phon_col = (240, 230, 240)
volna_col = (0, 250, 0)
poplavok_col = (240, 120, 240)
knopka_col = (110, 200, 240)

# загружаю данные с json
dop_file = "waves.json"
with open(dop_file) as f:
    dop_data = json.load(f)

# проверяю ключи в json
kolvo_voln = dop_data.get("number of waves", 5)
property_voln = dop_data.get("waves", [{"amplitude": 20, "period": 100, "speed": 1}] * kolvo_voln)
poplavok_radius = dop_data.get("poplavok radius", 10)

# пишу данные волн и поплавков :3
poplavok_positions = [dlina // (kolvo_voln + 1) * (i + 1) for i in range(kolvo_voln)]
poplavok_ves = [random.uniform(0.5, 2.0) for _ in range(kolvo_voln)]
poplavok_x_positions = [0] * kolvo_voln
selected_poplavok = None
selected_volna = None

# пишу всё, что связано с интерфейсом
class UI_knopka:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback

    def draw(self, surface):
        pygame.draw.rect(surface, knopka_col, self.rect)
        font = pygame.font.Font(None, 20)
        text_surf = font.render(self.text, True, (0, 0, 200))
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def click_obrabotka(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

class UI_polzynok:
    def __init__(self, x, y, width, min_znach, max_znach, initial_value):
        self.rect = pygame.Rect(x, y, width, 10)
        self.knob_rect = pygame.Rect(x, y - 5, 10, 20)
        self.min_znach = min_znach
        self.max_znach = max_znach
        self.znach = initial_value
        self.dragging = False
        self.obrabotka_knopki()

    def obrabotka_knopki(self):
        knob_center_x = self.rect.left + (self.znach - self.min_znach) / (self.max_znach - self.min_znach) * self.rect.width
        self.knob_rect.centerx = int(knob_center_x)

    def draw(self, surface):
        pygame.draw.rect(surface, knopka_col, self.rect)
        pygame.draw.rect(surface, (100, 100, 100), self.knob_rect)

    def click_obrabotka(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.knob_rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.knob_rect.centerx = max(self.rect.left, min(self.rect.right, event.pos[0]))
            self.znach = self.min_znach + (self.knob_rect.centerx - self.rect.left) / self.rect.width * (self.max_znach - self.min_znach)

    def get_znach(self):
        return self.znach

    def set_znach(self, znach):
        self.znach = znach
        self.obrabotka_knopki()

# сбрасываю вес поплавка
def sbros_poplavka():
    global selected_poplavok
    if selected_poplavok is not None:
        poplavok_ves[selected_poplavok] = 1.0
        polzynok_vesa.set_znach(1.0)

# добавляю волны
def add_voln():
    global property_voln, poplavok_positions, poplavok_ves, poplavok_x_positions
    property_voln.append({"amplitude": 20, "period": 100, "speed": 1})
    new_position = random.randint(50, dlina - 50)
    while any(abs(new_position - pos) < 50 for pos in poplavok_positions):
        new_position = random.randint(50, dlina - 50)
    poplavok_positions.append(new_position)
    poplavok_ves.append(1.0)
    poplavok_x_positions.append(0)

# удаляю волны
def delete_voln():
    global property_voln, poplavok_positions, poplavok_ves, poplavok_x_positions
    if property_voln:
        property_voln.pop()
        poplavok_positions.pop()
        poplavok_ves.pop()
        poplavok_x_positions.pop()

# интерфейс элементов
knopka_sbrosa = UI_knopka(10, 10, 100, 30, "сброс массы", sbros_poplavka)
knopka_add_voln = UI_knopka(120, 10, 100, 30, "добавить волну", add_voln)
knopka_delete_voln = UI_knopka(230, 10, 100, 30, "удалить волну", delete_voln)
polzynok_vesa = UI_polzynok(10, 50, 200, 0.5, 2.0, 1.0)
polzynok_amplituda = UI_polzynok(10, 100, 200, 10, 100, 20)
polzynok_period = UI_polzynok(10, 150, 200, 50, 300, 100)

# основной цикл
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(phon_col)

    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # проверка клика по поплавку
            for i, volna_y in enumerate(poplavok_positions):
                dx = abs(poplavok_x_positions[i] - event.pos[0])
                dy = abs(volna_y - event.pos[1])
                if dx < poplavok_radius and dy < poplavok_radius:
                    selected_poplavok = i
                    selected_volna = i
                    polzynok_vesa.set_znach(poplavok_ves[selected_poplavok])
                    polzynok_amplituda.set_znach(property_voln[selected_volna]["amplitude"])
                    polzynok_period.set_znach(property_voln[selected_volna]["period"])
        # обработка событий интерфейса
        knopka_sbrosa.click_obrabotka(event)
        knopka_add_voln.click_obrabotka(event)
        knopka_delete_voln.click_obrabotka(event)
        polzynok_vesa.click_obrabotka(event)
        polzynok_amplituda.click_obrabotka(event)
        polzynok_period.click_obrabotka(event)

    # обновление веса поплавка
    if selected_poplavok is not None:
        poplavok_ves[selected_poplavok] = polzynok_vesa.get_znach()

    # обновление амплитуды и периода волны
    if selected_volna is not None:
        property_voln[selected_volna]["amplitude"] = polzynok_amplituda.get_znach()
        property_voln[selected_volna]["period"] = polzynok_period.get_znach()

    # отображение интерфейса
    knopka_sbrosa.draw(screen)
    knopka_add_voln.draw(screen)
    knopka_delete_voln.draw(screen)
    polzynok_vesa.draw(screen)
    polzynok_amplituda.draw(screen)
    polzynok_period.draw(screen)

    # обновление волн и поплавков
    past_time = pygame.time.get_ticks() / 1000
    for i, volna in enumerate(property_voln):
        amplitude = volna["amplitude"]
        period = volna["period"]
        speed = volna["speed"]

        volna_y = poplavok_positions[i]
        for x in range(shirina):
            y = volna_y + amplitude * math.sin(2 * math.pi * (x / period) - speed * past_time)
            pygame.draw.circle(screen, volna_col, (x, int(y)), 1)

        # учитываю вес для скорости поплавка
        redact_speed = 100 / poplavok_ves[i]
        poplavok_x_positions[i] = (past_time * redact_speed) % shirina
        effect_volna_y = volna_y + amplitude * math.sin(2 * math.pi * (poplavok_x_positions[i] / period) - speed * past_time)
        poplavok_y = effect_volna_y + poplavok_ves[i] * 5
        pygame.draw.circle(screen, poplavok_col, (int(poplavok_x_positions[i]), int(poplavok_y)), poplavok_radius)

    pygame.display.update()
    clock.tick(60)

pygame.quit()

# конец... ;(
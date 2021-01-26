import pygame
import random

# инициализация цветов
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)
pink = (255, 0, 255)

color = [red, green, blue, yellow, black, pink]
cur_color = 0
# объявление переменных
n = 30
m = 30

width = 600
height = 600
# создание окна
screen = pygame.display.set_mode((width, height + 150))
pygame.font.init()
pygame.display.set_caption('Игра Жизнь')
font = pygame.font.SysFont('Times New Roman', 30)

rules_img = pygame.image.load('game of life rules.png')
theory_img = pygame.image.load('game of life theory.png')
# создание поля
table = []
for i in range(n):
    table.append([])
    for j in range(m):
        table[i].append(0)

speed = 500
nabes = [[1, 1], [1, 0], [0, 1], [-1, -1], [-1, 0], [0, -1], [1, -1], [-1, 1]]
run = False
guide = False
theory = False


def createButton(pos, size, text):  # метод для создания кнопки
    button = pygame.draw.rect(screen, white, [pos[0], pos[1], size[0], size[1]])
    surf = font.render(text, False, black)
    screen.blit(surf, (pos[0] + 5, pos[1] + 5))
    return button


def next(pos):  # метод для определения последующего состояния клетки
    res = 0
    for nabe in nabes:
        res += table[(pos[0] + nabe[0]) % n][(pos[1] + nabe[1]) % m]
    if (table[pos[0]][pos[1]] == 1 and 2 <= res <= 3) or (table[pos[0]][pos[1]] == 0 and res == 3):
        return 1
    return 0


def refreshTable():  # метод выводящий текущее состояние доски на поле
    for i in range(n):
        for j in range(m):
            if table[i][j]:
                pygame.draw.rect(screen, color[cur_color], [i * 20, j * 20, 20, 20])
    pygame.display.update()


while True:  # основной цикл
    screen.fill(white)

    # отрисовка поля
    for i in range(n + 1):
        pygame.draw.line(screen, black, (0, i * 20), (width, i * 20))
    for i in range(m):
        pygame.draw.line(screen, black, (i * 20, 0), (i * 20, height))

    # создание кнопок
    run_button = createButton((25, 630), (60, 40), "Run")
    stop_button = createButton((130, 630), (70, 40), "Stop")
    rand_gen = createButton((30, 690), (110, 40), "Generate")
    speed_inc = createButton((360, 630), (100, 40), "Speed+")
    speed_dec = createButton((490, 630), (100, 40), "Speed-")
    reset_button = createButton((240, 630), (110, 40), "Reset")
    color_change = createButton((470, 690), (90, 40), "Color")
    guide_button = createButton((180, 690), (110, 40), "Guidance")
    theory_button = createButton((340, 690), (90, 40), "Theory")

    for event in pygame.event.get():  # цикл обработчика событий
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if guide or theory:
                guide = False
                theory = False
                continue
            if event.pos[0] <= width and event.pos[1] <= height and not run:
                pos = [event.pos[0] // 20, event.pos[1] // 20]
                table[pos[0]][pos[1]] = (table[pos[0]][pos[1]] + 1) % 2
            elif run_button.collidepoint(event.pos):
                run = True
            elif stop_button.collidepoint(event.pos):
                run = False
            elif speed_inc.collidepoint(event.pos):
                speed = max(speed - 100, 20)
            elif speed_dec.collidepoint(event.pos):
                speed = min(speed + 100, 1000)
            elif rand_gen.collidepoint(event.pos):
                for i in range(n):
                    for j in range(m):
                        table[i][j] = random.randint(0, 1)
                refreshTable()
            elif reset_button.collidepoint(event.pos):
                for i in range(n):
                    for j in range(m):
                        table[i][j] = 0
                refreshTable()
            elif color_change.collidepoint(event.pos):
                cur_color = (cur_color + 1) % len(color)
            elif guide_button.collidepoint(event.pos):
                guide = True
            elif theory_button.collidepoint(event.pos):
                theory = True

    if guide:
        screen.fill(white)
        screen.blit(rules_img, (0, 0))
        pygame.display.update()
    elif theory:
        screen.fill(white)
        screen.blit(theory_img, (0, 0))
        pygame.display.update()

    if run and not guide and not theory:  # обновление состояния поля
        table_upd = []
        for i in range(n):
            table_upd.append([])
            for j in range(m):
                table_upd[i].append(next([i, j]))
        if table == table_upd:
            run = False
        table = table_upd
        pygame.time.wait(speed)  # задержка определяемая скоростью игры
    if not guide and not theory:
        refreshTable()  # отрисвка поля

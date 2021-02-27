# Нужные модули и библиотеки
import pygame
from pygame.math import Vector2
import random

pygame.init()

SCHRIFT = pygame.font.SysFont('Times New Roman', 26)
FPS = 60

SCORE_WIDTH = 1200
SCORE_HEIGHT = 640
DISP = (SCORE_WIDTH, SCORE_HEIGHT)

RED = (150, 0, 0)
BLACK = (0, 0, 0)
GRAY = (80, 80, 80)
WHITE = (255, 255, 255)

MaxScore = 10


class Ball(pygame.sprite.Sprite):  # Класс мяча

    def __init__(self, w, h):  # w - width, h - height
        super().__init__()
        self.w, self.h = w, h
        self.image = pygame.Surface([10, 10])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.initialize()

    def initialize(self):  # Значения старта и конца, выход за поле игры
        self.dir_to = random.choice([Vector2(-10, -10), Vector2(10, -10), Vector2(-10, 10), Vector2(10, 10)])
        self.coords = Vector2(SCORE_WIDTH / 2, SCORE_HEIGHT / 2)
        self.rect.center = self.coords
        self.udary = 0
        self.skorost = 1.0

    def update(self):  # Обновление координат
        if self.coords.y <= 10:  # Нижняя и верхняя граница
            self.dir_to = random.choice([Vector2(-10, 10), Vector2(10, 10)])
        if self.coords.y >= self.h - 10:
            self.dir_to = random.choice([Vector2(-10, -10), Vector2(10, -10)])

        self.coords += self.dir_to * self.skorost
        self.rect.center = self.coords

    def udar(self):  # Действие при ударе
        self.udary += 1
        self.skorost = 1.0 + self.udary / 10


class User(pygame.sprite.Sprite):  # Класс игроков

    def __init__(self, num, w, h):
        super().__init__()
        self.racket_parametr = 150
        self.skorost_sdviga = 20

        gr = 50

        self.image = pygame.Surface([20, self.racket_parametr])  # Ракетки
        self.image.fill(RED)

        self.schet = 0  # Счет
        self.w, self.h = w, h

        if num != 'Left':  # Стороны отображения ракеток
            self.pos = Vector2(self.w - gr - 10, self.h / 2)
        else:
            self.pos = Vector2(gr, self.h / 2)
        self.rect = self.image.get_rect(topleft=self.pos)

    def vniz(self):
        if self.pos.y + self.racket_parametr < self.h:  # Движение вниз
            self.rect.top = self.pos.y
            self.pos.y += self.skorost_sdviga

    def vverh(self):
        if self.pos.y > 0:  # Движение вверх
            self.pos.y -= self.skorost_sdviga
            self.rect.top = self.pos.y


# Функция действий при окончании игры

def end_of_game(screen, winner, left_player, right_player):
    gray_fin = pygame.Surface((SCORE_WIDTH, SCORE_HEIGHT))
    gray_fin.fill(GRAY)
    gray_fin.set_colorkey(GRAY)
    gray_fin.set_alpha(99)
    pygame.draw.rect(gray_fin, BLACK, [0, 0, SCORE_WIDTH, SCORE_HEIGHT])
    schrift = pygame.font.SysFont(None, 100)
    end_of_game = schrift.render('{} игрок победил!'.format(winner), True, BLACK)
    score_schet = schrift.render(
        '{} - {}'.format(left_player.schet, right_player.schet), True, BLACK)
    screen.blit(score_schet, (SCORE_WIDTH / 2 - 50, SCORE_HEIGHT / 2 + 100))
    screen.blit(gray_fin, (0, 0))
    screen.blit(end_of_game, (SCORE_WIDTH / 2 - 250, SCORE_HEIGHT / 2 - 100))
    pygame.display.update()
    pygame.time.delay(10000)
    # Программа, для удобства, сама завершает работу через некоторое время,
    # после оглашений финального счета и победителя


def schet_draw(left_player, right_player, schrift):  # Функция счета
    right_player_score = schrift.render(str(right_player.schet), True, BLACK)
    left_player_score = schrift.render(str(left_player.schet), True, BLACK)
    return left_player_score, right_player_score


def main():  # Главная функция игры
    screen = pygame.display.set_mode(DISP, 0, 32)
    time = pygame.time.Clock()

    # Положение мяча и ракеток

    left_player = User('Left', SCORE_WIDTH, SCORE_HEIGHT)
    right_player = User('Right', SCORE_WIDTH, SCORE_HEIGHT)
    ball = Ball(SCORE_WIDTH, SCORE_HEIGHT)

    all_sprites = pygame.sprite.Group(left_player, right_player, ball)

    # Текст

    text = SCHRIFT.render(str(MaxScore), True, BLACK)
    left_player_score, right_player_score = schet_draw(
        left_player, right_player, SCHRIFT)

    flag = False

    while not flag:
        for event in pygame.event.get():  # Основной цикл
            if event.type == pygame.QUIT:
                flag = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            flag = True

        if keys[pygame.K_w]:
            left_player.vverh()

        if keys[pygame.K_s]:
            left_player.vniz()

        if keys[pygame.K_UP]:
            right_player.vverh()

        if keys[pygame.K_DOWN]:
            right_player.vniz()

        # Игровая логика
        all_sprites.update()
        # Определение победителя
        if left_player.schet >= MaxScore or right_player.schet >= MaxScore:
            if left_player.schet > right_player.schet:
                winner = 'Левый'
            else:
                winner = 'Правый'
            end_of_game(screen, winner, left_player, right_player)
            flag = True

        # Столкновения, физика
        cl = ball.rect.colliderect(left_player.rect)
        cr = ball.rect.colliderect(right_player.rect)
        if cr or cl:
            ball.dir_to.x *= -1
            ball.udar()

        if ball.rect.x <= 0:  # Левая граница
            right_player.schet += 1
            ball.initialize()
            left_player_score, right_player_score = schet_draw(
                left_player, right_player, SCHRIFT)
        elif ball.rect.x >= SCORE_WIDTH:  # Правая граница
            left_player.schet += 1
            ball.initialize()
            left_player_score, right_player_score = schet_draw(
                left_player, right_player, SCHRIFT)

        # Отрисовка
        screen.fill(WHITE)
        screen.blit(left_player_score, (SCORE_WIDTH / 2 - 100, 10))
        screen.blit(right_player_score, (SCORE_WIDTH / 2 + 100, 10))
        screen.blit(text, (SCORE_WIDTH / 2, 0))
        all_sprites.draw(screen)
        # Текст окна, отображение текущего FPS
        pygame.display.set_caption('Рандомный пинг-понг / Текущий FPS - {}'.format(time.get_fps()))

        pygame.display.flip()
        time.tick(FPS)


if __name__ == '__main__':
    main()
    pygame.quit()

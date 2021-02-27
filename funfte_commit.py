import pygame
from pygame.math import Vector2
import random

pygame.init()

SCHRIFT = pygame.font.SysFont('Times New Roman', 26)
FPS = 60

SCORE_WIDTH = 1200
SCORE_HEIGHT = 640
DISP = (SCORE_WIDTH, SCORE_HEIGHT)

W = (150, 0, 0)
t = (0, 0, 0)
GRAY = (80, 80, 80)

MS = 10


class Ball(pygame.sprite.Sprite):

    def __init__(self, w, h):
        super().__init__()
        self.w, self.h = w, h
        self.image = pygame.Surface([10, 10])
        self.image.fill(t)
        self.rect = self.image.get_rect()
        self.initialize()

    def initialize(self):  # Значения старта и конца, выход за поле игры
        self.dir_to = random.choice([Vector2(-10, -10), Vector2(10, -10), Vector2(-10, 10), Vector2(10, 10)])
        self.coords = Vector2(SCORE_WIDTH / 2, SCORE_HEIGHT / 2)
        self.rect.center = self.coords
        self.udary = 0
        self.skorost = 1.0

    def update(self):
        if self.coords.y <= 10:  # Нижняя и верхняя граница
            self.dir_to = random.choice([Vector2(-10, 10), Vector2(10, 10)])
        if self.coords.y >= self.h - 10:
            self.dir_to = random.choice([Vector2(-10, -10), Vector2(10, -10)])

        self.coords += self.dir_to * self.skorost
        self.rect.center = self.coords

    def udar(self):
        self.udary += 1
        self.skorost = 1.0 + self.udary / 10


class User(pygame.sprite.Sprite):

    def __init__(self, num, w, h):
        super().__init__()
        self.real = 150
        self.skorost_sdviga = 20

        gr = 50

        self.image = pygame.Surface([20, self.real])
        self.image.fill(W)

        self.schet = 0
        self.w, self.h = w, h

        if num != 'Left':
            self.pos = Vector2(self.w - gr - 10, self.h / 2)
        else:
            self.pos = Vector2(gr, self.h / 2)
        self.rect = self.image.get_rect(topleft=self.pos)

    def vniz(self):
        if self.pos.y + self.real < self.h:  # Движение вниз
            self.rect.top = self.pos.y
            self.pos.y += self.skorost_sdviga

    def vverh(self):
        if self.pos.y > 0:  # Движение вверх
            self.pos.y -= self.skorost_sdviga
            self.rect.top = self.pos.y


def end_of_game(screen, winner, lp, rp):
    gray_fin = pygame.Surface((SCORE_WIDTH, SCORE_HEIGHT))
    gray_fin.fill(GRAY)
    gray_fin.set_colorkey(GRAY)
    gray_fin.set_alpha(99)
    pygame.draw.rect(gray_fin, t, [0, 0, SCORE_WIDTH, SCORE_HEIGHT])
    schrift = pygame.font.SysFont(None, 100)
    end_of_game = schrift.render('{} игрок победил!'.format(winner), True, t)
    score_schet = schrift.render(
        '{} - {}'.format(lp.schet, rp.schet), True, t)
    screen.blit(score_schet, (SCORE_WIDTH / 2 - 50, SCORE_HEIGHT / 2 + 100))
    screen.blit(gray_fin, (0, 0))
    screen.blit(end_of_game, (SCORE_WIDTH / 2 - 250, SCORE_HEIGHT / 2 - 100))
    pygame.display.update()
    pygame.time.delay(10000)


def schet_draw(lp, rp, schrift):  # Счет
    rps = schrift.render(str(rp.schet), True, t)
    lps = schrift.render(str(lp.schet), True, t)
    return lps, rps


def main():
    screen = pygame.display.set_mode(DISP, 0, 32)
    time = pygame.time.Clock()

    lp = User('Left', SCORE_WIDTH, SCORE_HEIGHT)
    rp = User('Right', SCORE_WIDTH, SCORE_HEIGHT)
    ball = Ball(SCORE_WIDTH, SCORE_HEIGHT)

    all_sprites = pygame.sprite.Group(lp, rp, ball)

    text = SCHRIFT.render(str(MS), True, t)
    lps, rps = schet_draw(
        lp, rp, SCHRIFT)

    flag = False

    while not flag:
        for event in pygame.event.get():  # Основной цикл
            if event.type == pygame.QUIT:
                flag = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            flag = True

        if keys[pygame.K_w]:
            lp.vverh()

        if keys[pygame.K_s]:
            lp.vniz()

        if keys[pygame.K_UP]:
            rp.vverh()

        if keys[pygame.K_DOWN]:
            rp.vniz()

        # Физика
        all_sprites.update()
        # Определение победителя
        if lp.schet >= MS or rp.schet >= MS:
            if lp.schet > rp.schet:
                winner = 'Левый'
            else:
                winner = 'Правый'
            end_of_game(screen, winner, lp, rp)
            flag = True

        # Столкновения, физика
        cl = ball.rect.colliderect(lp.rect)
        cr = ball.rect.colliderect(rp.rect)
        if cr or cl:
            ball.dir_to.x *= -1
            ball.udar()

        if ball.rect.x <= 0:  # Левая граница
            rp.schet += 1
            ball.initialize()
            lps, rps = schet_draw(
                lp, rp, SCHRIFT)
        elif ball.rect.x >= SCORE_WIDTH:  # Правая граница
            lp.schet += 1
            ball.initialize()
            lps, rps = schet_draw(
                lp, rp, SCHRIFT)

        # Отрисовка
        screen.fill((255, 255, 255))
        screen.blit(lps, (SCORE_WIDTH / 2 - 100, 10))
        screen.blit(rps, (SCORE_WIDTH / 2 + 100, 10))
        screen.blit(text, (SCORE_WIDTH / 2, 0))
        all_sprites.draw(screen)

        pygame.display.set_caption('Рандомный пинг-понг / Текущий FPS - {}'.format(time.get_fps()))

        pygame.display.flip()
        time.tick(FPS)


if __name__ == '__main__':
    main()
    pygame.quit()

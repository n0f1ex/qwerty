import random
import pygame
from pygame.math import Vector2

pygame.init()

FONT = pygame.font.SysFont('Times New Roman', 26)
FPS = 60

SCORE_WIDTH = 1200
SCORE_HEIGHT = 640
DISP = (SCORE_WIDTH, SCORE_HEIGHT)

W = (150, 0, 0)
t = (0, 0, 0)

MS = 10


class Ball(pygame.sprite.Sprite):

    def __init__(self, w, h):
        super().__init__()
        self.w, self.h = w, h
        self.image = pygame.Surface([10, 10])

        self.image.fill(t)  # Создание поля
        self.rect = self.image.get_rect()
        self.initialize()

    def initialize(self):
        #  Возврат начальных значений мяча при перезапуске игры и
        #  печать результата при окончании игры
        self.direction = random.choice(
            [Vector2(-10, -10), Vector2(10, -10),
             Vector2(-10, 10), Vector2(10, 10)])  # Выбор направления движения

        self.position_to_go = Vector2(SCORE_WIDTH / 2, SCORE_HEIGHT / 2)
        self.rect.center = self.position_to_go  # Начальная позиция

        self.udary = 0
        self.speed_up = 0.4

    def udar(self):
        self.speed_up = 1.0 + self.udary / 10
        self.udary = self.udary + 1

    def update(self):
        if self.position_to_go.y >= self.h - 10:  # Верхняя граница
            self.direction = random.choice([Vector2(-10, -10), Vector2(10, -10)])

        if self.position_to_go.y <= 10:  # Нижняя граница
            self.direction = random.choice([Vector2(-10, 10), Vector2(10, 10)])

        self.rect.center = self.position_to_go
        self.position_to_go = self.position_to_go + (self.direction * self.speed_up)


class User(pygame.sprite.Sprite):

    def __init__(self, num, w, h):
        super().__init__()
        self.rh = 150
        self.move_speed = 20

        gr = 50

        self.image = pygame.Surface([10, self.rh])
        self.image.fill(W)

        self.score = 0
        self.w, self.h = w, h

        if num != 'Left':
            self.pos = Vector2(self.w - gr - 10, self.h / 2)
        else:
            self.pos = Vector2(gr, self.h / 2)
        self.rect = self.image.get_rect(topleft=self.pos)

    def vverh(self):
        if self.pos.y > 0:  # Движение вверх
            self.pos.y -= self.move_speed
            self.rect.top = self.pos.y

    def vniz(self):
        if self.pos.y + self.rh < self.h:  # Движение вниз
            self.rect.top = self.pos.y
            self.pos.y += self.move_speed

def render_score(lp, rp, font):  # Счет
    lps = font.render(str(lp.score), True, (0, 0, 0))
    rps = font.render(str(rp.score), True, (0, 0, 0))
    return lps, rps

def main():
    screen = pygame.display.set_mode(DISP, 0, 32)

    clock = pygame.time.Clock()

    lp = User('Left', SCORE_WIDTH, SCORE_HEIGHT)
    rp = User('Right', SCORE_WIDTH, SCORE_HEIGHT)
    ball_go = Ball(SCORE_WIDTH, SCORE_HEIGHT)

    all_sprites = pygame.sprite.Group(lp, rp, ball_go)

    gt = FONT.render(str(MS), True, (255, 255, 0))
    lps, rps = render_score(lp, rp, FONT)

    flag = False

    while not flag:
        # Совершение действия
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = True

        key = pygame.key.get_pressed()
        if key[pygame.K_e]:
            flag = True

        if key[pygame.K_w]:
            lp.vverh()

        if key[pygame.K_s]:
            lp.vniz()

        if key[pygame.K_UP]:
            rp.vverh()

        if key[pygame.K_DOWN]:
            rp.vniz()

        all_sprites.update()

        screen.fill((200, 200, 200)) #  Часть графики
        screen.blit(lps, (SCORE_WIDTH / 2 - 100, 10))
        screen.blit(rps, (SCORE_WIDTH / 2 + 100, 10))
        screen.blit(gt, (SCORE_WIDTH / 2, 0))
        all_sprites.draw(screen)

        pygame.display.set_caption('Пинг-понг {}'.format(clock.get_fps()))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
    pygame.quit()

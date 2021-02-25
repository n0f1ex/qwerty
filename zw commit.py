import random
import pygame
from pygame.math import Vector2


pygame.init()

FONT = pygame.font.SysFont('Arial', 26)
FPS = 30
SCORE_WIDTH = 1200
SCORE_HEIGHT = 640
DISP = (SCORE_WIDTH, SCORE_HEIGHT)
white = (230, 210, 190)

class Ball(pygame.sprite.Sprite):

    def __init__(self, width, height):
        super().__init__()
        self.width, self.height = width, height
        self.image = pygame.Surface([10, 10])
        self.image.fill(white) #Создание поля
        self.rect = self.image.get_rect()
        self.initialize()

    def initialize(self):
        """ Сделать возврат начальных значений мяча при перезапуске игры и
            печать результата при окончании игры"""
        self.direction = random.choice(
            [Vector2(-10, -10), Vector2(10, -10),
             Vector2(-10, 10), Vector2(10, 10)]) #Выбор направления движения
        self.position = Vector2(SCORE_WIDTH/2, SCORE_HEIGHT/2)
        self.rect.center = self.position #Начальная позиция

class User(pygame.sprite.Sprite):

    def __init__(self, num, width, height):
        super().__init__()
        self.score = 0
        self.width, self.height = width, height
        self.rack_height = 100
        self.move_speed = 20
        offset = 20
        self.image = pygame.Surface([10, self.rack_height])
        self.image.fill(white)

        if num == 'Left':
            self.pos = Vector2(offset, self.height/2)
        else:
            self.pos = Vector2(self.width-offset-10, self.height/2)
        self.rect = self.image.get_rect(topleft=self.pos)

    def move_up(self):
        if self.pos.y > 0:
            self.pos.y -= self.move_speed
            self.rect.top = self.pos.y

    def move_down(self):
        if self.pos.y + self.rack_height < self.height:
            self.pos.y += self.move_speed
            self.rect.top = self.pos.y

def main():
    screen = pygame.display.set_mode(DISP, 0, 32)
    clock = pygame.time.Clock()

    left_user = User('Left', SCORE_WIDTH, SCORE_HEIGHT)
    right_user = User('Right', SCORE_WIDTH, SCORE_HEIGHT)
    curr_ball = Ball(SCORE_WIDTH, SCORE_HEIGHT)

    all_sprites = pygame.sprite.Group(left_user, right_user, curr_ball)

    flag = False

    while not flag:
        # Совершение действия
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = True

        key = pygame.key.get_pressed()
        if key[pygame.K_e]:
            flag = True
        if key[pygame.K_UP]:
            right_user.move_up()
        if key[pygame.K_DOWN]:
            right_user.move_down()
        if key[pygame.K_w]:
            left_user.move_up()
        if key[pygame.K_s]:
            left_user.move_down()

        all_sprites.update()

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        pygame.display.set_caption('Ping Pong {}'.format(clock.get_fps()))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
    pygame.quit()

import random
import pygame
from pygame.math import Vector2


pygame.init()

FONT = pygame.font.SysFont('Arial', 26)
FPS = 30
SCORE_WIDTH = 800
SCORE_HEIGHT = 640
DISP = (SCORE_WIDTH, SCORE_HEIGHT)
white = (255, 255, 255)

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

class Player(pygame.sprite.Sprite):

    def __init__(self, width, height):
        super().__init__()
        self.score = 0
        self.width, self.height = width, height

def main():
    screen = pygame.display.set_mode(DISP, 0, 32)
    clock = pygame.time.Clock()

    done = False

    while not done:
        # Совершение действия
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.set_caption('Ping Pong {}'.format(clock.get_fps()))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
    pygame.quit()
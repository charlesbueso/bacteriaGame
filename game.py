import pygame
import time
import math
import random

WIDTH = 900
HEIGHT = 750

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bacteria Game!")

# main game loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        # checks images and get rect... self.rect.center = (winWidth / 2, winHeight / 2) #self.rect.bottom = winHeight
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
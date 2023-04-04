import pygame
import time
import math
import random

pygame.init()

WIDTH = 900
HEIGHT = 750
fps = 60
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Bacteria Game!")
timer = pygame.time.Clock()


# main game loop
running = True
while running:

    screen.fill('white')
    timer.tick(fps)
    mousePosition = pygame.mouse.get_pos()
    pygame.draw.circle(screen, 'red', mousePosition, 10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill('white')
        self.rect = self.image.get_rect()
        # checks images and get rect... self.rect.center = (winWidth / 2, winHeight / 2) #self.rect.bottom = winHeight
        self.rect.center = (WIDTH / 2, HEIGHT / 2)


pygame.quit()
import pygame
import time
import math
import random

#Global variables
WIDTH = 900
HEIGHT = 750
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
bacteriaVelocity = 22
pygame.display.set_caption("Bacteria Game!")
pygame.mouse.set_visible(True)

class Bacteria(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30,30))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        # checks images and get rect... self.rect.center = (winWidth / 2, winHeight / 2) #self.rect.bottom = winHeight
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.movex = 0 # move along X
        self.movey = 0 # move along Y
        self.frame = 0 # count frames
        self.speed = 1.5 # speed of the bacteria

    def update(self):

        # current mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
            
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        dist = ((dx ** 2) + (dy ** 2)) ** 0.5 # distance between the mouse and the bacteria (Pythagorean theorem)
        
        if dist > self.speed:
            self.rect.centerx += dx * self.speed / dist
            self.rect.centery += dy * self.speed / dist
        else:
            self.rect.centerx = mouse_x
            self.rect.centery = mouse_y

        

class Antidote(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30,30))
        self.image.fill('blue')
        self.rect = self.image.get_rect()
        # checks images and get rect... self.rect.center = (winWidth / 2, winHeight / 2) #self.rect.bottom = winHeight
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.movex = 0 # move along X
        self.movey = 0 # move along Y
        self.frame = 0 # count frames

    #Missing update function
    #Will update movement of antidotes, as well as random spawns(?) and size mutations(?)
    #def update():
         
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        #offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        #background
        self.ground_surf = pygame.image.load('whiteBackground.jpg').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))
    
    def center_target_camera(self,target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self,player):
        
        self.center_target_camera(player)

        #ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf,ground_offset)

        #active elements
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)



pygame.init()

all_sprites_list = pygame.sprite.Group()
bacteria = Bacteria()
Bacteria.image = pygame.Surface([30, 30])
Bacteria.rect = Bacteria.image.get_rect()
camera = CameraGroup()
all_sprites_list.add(bacteria)

mutationCounter = 0


# main game loop
running = True
while running:

    screen.fill('white')
    timer.tick(fps)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    camera.update()
    camera.custom_draw(bacteria)

    all_sprites_list.update()
    all_sprites_list.draw(screen)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()

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
pygame.display.set_caption("Bacteria Game!")
pygame.mouse.set_visible(False)

class Bacteria(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30,30))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        # checks images and get rect... self.rect.center = (winWidth / 2, winHeight / 2) #self.rect.bottom = winHeight
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
         mousePosition = pygame.mouse.get_pos()
         self.rect.x = mousePosition[0]
         self.rect.y = mousePosition[1]

class Antidote(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30,30))
        self.image.fill('blue')
        self.rect = self.image.get_rect()
        # checks images and get rect... self.rect.center = (winWidth / 2, winHeight / 2) #self.rect.bottom = winHeight
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    #Must find offset between player center and game box, substract to other side
    #def update(self):
    #     mousePosition = pygame.mouse.get_pos()
    #     self.rect.x = mousePosition[0]
    #     self.rect.y = mousePosition[1]
         
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



pygame.init()

all_sprites_list = pygame.sprite.Group()
bacteria = Bacteria()
camera = CameraGroup()
all_sprites_list.add(bacteria)

# main game loop
running = True
while running:

    screen.fill('white')
    timer.tick(fps)
    
    camera.update()
    camera.custom_draw(bacteria)

    all_sprites_list.update()
    all_sprites_list.draw(screen)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()

def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

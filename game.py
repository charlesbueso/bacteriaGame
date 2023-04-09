import pygame
import time
import math
import random
import sys

#Global variables
WIDTH = 900
HEIGHT = 750
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
bacteriaVelocity = 22
pygame.display.set_caption("Bacteria Game!")
pygame.mouse.set_visible(True)
foodColors = [(155,93,229), (241, 91, 181), (254,228, 64), (0,187,249), (0,245,212)] #food colors
antidoteColor = (0, 0, 0) #antidote color: black
food_data = [] #stores food positions and colors
antidote_data = [] #stores antidote positions and colors
mutation_data = [] #stores mutation positions and colors
antidoteImage = pygame.image.load("antidote.png")
mutationImage = pygame.image.load("mutation.png")

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

    #Missing update function
    #Will update movement of antidotes, as well as random spawns(?) and size mutations(?)

#TODO: Add movement of antidotes? and randomize size        
class Antidote(pygame.sprite.Sprite):
    def __init__(self, x, y, color, group):
        super().__init__(group)
        self.image = pygame.Surface((30, 30))
        self.image = antidoteImage
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #TODO:maybe needs an update function?

    # def update(self):
    #     checkCollision(self.rect.center, food_data)
    #     mouse_x, mouse_y = pygame.mouse.get_pos()
    #     dx = 0
    #     dy = 0  

    #Missing update function
    #Will update movement of antidotes, as well as random spawns(?) and size mutations(?)

def createAntidote_Data(antidote_list, n):
    for i in range(n):
        while True:
            x = random.randrange(0, 1200)
            y = random.randrange(0, 1500)
            antidoteExists = False
            for antidote in antidote_list:
                if (x, y) == antidote[0:2]: #checks if the antidote (x, y) is already in the list
                    antidoteExists = True #breaks out of the loop to go back to the while loop (so we can regenerate an x & y)
                    break
            if not antidoteExists: #breaks out of the loop if the antidote doesn't exist so we can append it to the list
                break
            
        antidote_list.append((x, y, antidoteColor)) #add data to list

def createAntidote_Obj(antidote_list, antidoteGroup, cameraGroup):
    for i in range(len(antidote_list)):
        antidoteGroup.add(Antidote(antidote_list[i][0], antidote_list[i][1], antidote_list[i][2], cameraGroup))

class food(pygame.sprite.Sprite):
    def __init__(self, x, y, color, group):
        super().__init__(group)
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #TODO:maybe needs an update function?

def createFood_Data(food_list, n): # creats a list of random food locations, colors, and sizes    
     for i in range(n):
        while True:
             x = random.randrange(0, 1200)
             y = random.randrange(0, 1500)
             foodExists = False
             for food in food_list:
                 if (x, y) == food[0:2]: #checks if the food (x, y) is already in the list
                     foodExists = True #breaks out of the loop to go back to the while loop (so we can regenerate an x & y)
                     break
             if not foodExists: #breaks out of the loop if the food doesn't exist so we can append it to the list
                 break
            
        food_list.append((x, y, random.choice(foodColors))) #add data to list

def createFood_Obj(food_list, foodGroup, cameraGroup): #creates food objects
    for i in range(len(food_list)):
        foodGroup.add(food(food_list[i][0], food_list[i][1], food_list[i][2], cameraGroup))

class mutation(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = pygame.Surface((20, 20))
        self.image = mutationImage
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #TODO:maybe needs an update function?

def createMutation_Data(mutation_list, n): #creates a list of random food locations, colors, and sizes    
    
     for i in range(n):
        while True:
             x = random.randrange(0, 1200)
             y = random.randrange(0, 1500)
             mutationExists = False
             for mutation in mutation_list:
                 if (x, y) == mutation[0:2]: #checks if the food (x, y) is already in the list
                     mutationExists = True #breaks out of the loop to go back to the while loop (so we can regenerate an x & y)
                     break
             if not mutationExists: #breaks out of the loop if the food doesn't exist so we can append it to the list
                 break
            
        mutation_list.append((x, y)) #add data to list

def createMutation_Obj(mutation_list, mutationGroup, cameraGroup): #creates food objects
    for i in range(len(mutation_list)):
        mutationGroup.add(mutation(mutation_list[i][0], mutation_list[i][1], cameraGroup))

def checkCollision(player, food): #not yet implemented
    for i in range(len(food)):
        if food[i][0] == player.x and food[i][1] == player.y:
            return True
    return False

         
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

def button(message,x,y,width,height,inactiveColor,activeColor,action=None):

    mouse_x, mouse_y = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+width > mouse_x > x and y+height > mouse_y > y:
        pygame.draw.rect(screen, activeColor,(x,y,width,height))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, inactiveColor,(x,y,width,height))

    smallText = pygame.font.Font("playbuttonfont.ttf",40)
    textSurf, textRect = text_objects(message, smallText)
    textRect.center = ((x+(width/2)), (y+(height/2)))
    screen.blit(textSurf, textRect)

def text_objects(text, font):

    textSurface = font.render(text, True, 'black')
    return textSurface, textSurface.get_rect()

def game_loop():
    #intro = False
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill('white')
        timer.tick(fps)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if len(food_data) < 100: #replenish food
            createFood_Data(food_data,random.randrange(150, 250))
            createFood_Obj(food_data, food_group, camera)
        
        if len(antidote_data) < 50: #replenish antidote enemies
            createAntidote_Data(antidote_data,random.randrange(40, 75))
            createAntidote_Obj(antidote_data, antidote_group, camera)

        if len(mutation_data) < 50: #replenish mutation enemies
            createMutation_Data(mutation_data,random.randrange(10, 20))
            createMutation_Obj(mutation_data, mutation_group, camera)
        
        camera.update()
        camera.custom_draw(bacteria)

        all_sprites_list.update()
        all_sprites_list.draw(screen)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:# if user hits red x button close window
                running = False
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:# if user hits a escape key close program
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()


        pygame.display.update()
        pygame.display.flip()


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill('white')
        largeText = pygame.font.Font('titlefont.ttf',100)
        TextSurf, TextRect = text_objects("Bacteria Game", largeText)
        TextRect.center = ((WIDTH/2),(HEIGHT/2))
        screen.blit(TextSurf, TextRect)

        button("PLAY",385,515,140,75,"yellow","green",game_loop)

        pygame.display.update()
        timer.tick(15)


pygame.init()

all_sprites_list = pygame.sprite.Group()
bacteria = Bacteria()
all_sprites_list.add(bacteria)
food_group = pygame.sprite.Group() # Define a sprite group ONLY for the food objects
antidote_group = pygame.sprite.Group() # Define a sprite group ONLY for the antidote objects
mutation_group = pygame.sprite.Group() # Define a sprite group ONLY for the mutation objects
camera = CameraGroup()
mutationCounter = 0

# menu
game_intro()
# main loop
game_loop()
# quit
pygame.quit()

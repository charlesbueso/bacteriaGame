import pygame
import time
import math
import random
import sys
import os

pygame.init()
pygame.font.init()

# Global variables
WIDTH = 900
HEIGHT = 750
screen = pygame.display.set_mode([WIDTH, HEIGHT])
defaultBar = pygame.Surface((300,40))
timer = pygame.time.Clock()
fps = 60
pygame.display.set_caption("E Colide")
pygame.mouse.set_visible(True)
foodColors = [(155, 93, 229), (241, 91, 181), (254, 228, 64), (0, 187, 249), (0, 245, 212)]  # food colors
antidoteColor = (0, 0, 0)  # antidote color: black
food_data = []  # stores food positions and colors
antidote_data = []  # stores antidote positions and colors
mutation_data = []  # stores mutation positions and colors
antidoteImages = [pygame.image.load("antidote.png"), pygame.image.load("RedGloop.PNG"), pygame.image.load("BluePill.PNG"), pygame.image.load("GreenPill.PNG"),pygame.image.load("PinkPill.PNG")]
mutationImage = pygame.image.load("mutation.png")
bacteriaImages = [pygame.image.load("bacteriaPng.png"), pygame.image.load("BlueBacteria.PNG"), pygame.image.load("GreenBacteria.PNG")]
backgroundImage = pygame.image.load('grid-background.png')
backgroundImage = pygame.transform.scale(backgroundImage,(WIDTH,HEIGHT))

gameover = False
bacteriaSize = (100,100)


class Bacteria(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(bacteriaSize)
        self.image = pygame.transform.scale(bacteriaImages[0],bacteriaSize)
        self.rect = self.image.get_rect()
        # checks images and get rect... self.rect.center = (winWidth / 2, winHeight / 2) #self.rect.bottom = winHeight
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.movex = 0  # move along X
        self.movey = 0  # move along Y
        self.frame = 0  # count frames
        self.speed = 1.5  # speed of the bacteria
        self.stShield = 100
        self.mutation_counter = 0
        self.size = bacteriaSize

    def update(self):

        # current mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        dist = ((dx ** 2) + (dy ** 2)) ** 0.5  # distance between the mouse and the bacteria (Pythagorean theorem)

        if dist > self.speed:
            self.rect.centerx += dx * self.speed / dist
            self.rect.centery += dy * self.speed / dist
        else:
            self.rect.centerx = mouse_x
            self.rect.centery = mouse_y

            # Missing update function
    # Will update movement of antidotes, as well as random spawns(?) and size mutations(?)

def eat(self,antidoteSize):
    addedSize = antidoteSize[0]
    print(addedSize)
    self.image = pygame.Surface(((bacteriaSize[0]+addedSize), (bacteriaSize[0]+addedSize)))
    self.image = pygame.transform.scale(bacteriaImages[0],(bacteriaSize[0]+addedSize, bacteriaSize[0]+addedSize))
    self.rect = self.image.get_rect()
    self.size = ((bacteriaSize[0]+addedSize), (bacteriaSize[0]+addedSize))
    self.mutation_counter += math.log(addedSize)

def check_collision(bacteria, antidotes_group):
    # Loop through all the Antidote sprites in the group
    for antidote in antidotes_group:
        # Check for collision between the Bacteria and the Antidote sprite
        if pygame.sprite.collide_rect(bacteria, antidote):
            # Check if the Antidote is smaller than the Bacteria
            if antidote.size < bacteria.size:
                # Increase the size of the Bacteria relative to the size of the Antidote
                bacteria.size += antidote.size
                bacteria.mutation_counter += 1
                bacteriaSize = ((bacteria.size[0] + antidote.size[0]), (bacteria.size[0] + antidote.size[0]))
                bacteria.image = pygame.Surface(bacteriaSize)
                bacteria.image = pygame.transform.scale(bacteriaImages[0],bacteriaSize)
                bacteria.rect = bacteria.image.get_rect()
                # Remove the Antidote sprite from the group
                antidotes_group.remove(antidote)
                antidote.kill()
                return True
            else:
                print('gameover')
                # The Antidote is bigger than the Bacteria, return False to indicate failure
                return False
    # No collision detected, return True to indicate success
    return True

class Antidote(pygame.sprite.Sprite):
    def __init__(self, x, y, color, group, size):
        super().__init__(group)
        self.image = pygame.Surface(size)
        randomImage = random.randint(0,len(antidoteImages)-1)
        self.image = pygame.transform.scale(antidoteImages[randomImage],size)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.velocity.x = random.uniform(-5, 5)
        self.velocity.y = random.uniform(-5, 5)
        self.size = size


    def update(self): #TODO find out the actual dimensions of the surface so their movement is not restricted.
         
        # Update the position of the Antidote
        self.rect.move_ip(self.velocity)

        #Wrap the Antidote around the screen edges
        #TODO update to bounce of the walls rather than wrapping
        if self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = HEIGHT


def createAntidote_Data(antidote_list):
    while len(antidote_list) < 15:
        while True:
            x = random.randrange(0, 1200)
            y = random.randrange(0, 1500)
            antidoteExists = False
            for antidote in antidote_list:
                if (x, y) == antidote[0:2]:  # checks if the antidote (x, y) is already in the list
                    antidoteExists = True  # breaks out of the loop to go back to the while loop (so we can regenerate an x & y)
                    break
            if not antidoteExists:  # breaks out of the loop if the antidote doesn't exist so we can append it to the list
                break

        antidote_list.append((x, y, antidoteColor))  # add data to list

def createAntidote_Obj(antidote_list, antidoteGroup, cameraGroup):
    for i in range(len(antidote_list)):
        randomSize = random.randint(bacteriaSize[0]-50,bacteriaSize[0]+20)
        antidoteGroup.add(Antidote(antidote_list[i][0], antidote_list[i][1], antidote_list[i][2], cameraGroup, (randomSize, randomSize)))
    

class food(pygame.sprite.Sprite):
    def __init__(self, x, y, color, group):
        super().__init__(group)
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)



def createFood_Data(food_list, n):  # creats a list of random food locations, colors, and sizes
    for i in range(n):
        while True:
            x = random.randrange(0, 1200)
            y = random.randrange(0, 1500)
            foodExists = False
            for food in food_list:
                if (x, y) == food[0:2]:  # checks if the food (x, y) is already in the list
                    foodExists = True  # breaks out of the loop to go back to the while loop (so we can regenerate an x & y)
                    break
            if not foodExists:  # breaks out of the loop if the food doesn't exist so we can append it to the list
                break

        food_list.append((x, y, random.choice(foodColors)))  # add data to list


def createFood_Obj(food_list, foodGroup, cameraGroup):  # creates food objects
    for i in range(len(food_list)):
        foodGroup.add(food(food_list[i][0], food_list[i][1], food_list[i][2], cameraGroup))


class mutation(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = pygame.Surface((20, 20))
        self.image = mutationImage
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.velocity.x = random.uniform(-5, 5)
        self.velocity.y = random.uniform(-5, 5)

    def update(self): #TODO find out the actual dimensions of the surface so their movement is not restricted.
        # Update the position of the Mutation
        self.rect.move_ip(self.velocity)

        #Wrap the Mutation around the screen edges 
        #TODO update to bounce of the walls rather than wrapping
        if self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = HEIGHT


def createMutation_Data(mutation_list, n):  # creates a list of random food locations, colors, and sizes

    for i in range(n):
        while True:
            x = random.randrange(0, 1200)
            y = random.randrange(0, 1500)
            mutationExists = False
            for mutation in mutation_list:
                if (x, y) == mutation[0:2]:  # checks if the food (x, y) is already in the list
                    mutationExists = True  # breaks out of the loop to go back to the while loop (so we can regenerate an x & y)
                    break
            if not mutationExists:  # breaks out of the loop if the food doesn't exist so we can append it to the list
                break

        mutation_list.append((x, y))  # add data to list


def createMutation_Obj(mutation_list, mutationGroup, cameraGroup):  # creates food objects
    for i in range(len(mutation_list)):
        mutationGroup.add(mutation(mutation_list[i][0], mutation_list[i][1], cameraGroup))


class defaultBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        topleft = ((WIDTH/2)*1.5)-150
        self.image = pygame.Surface((300,40)) #bar
        self.rect = pygame.Rect((topleft, 30),(300,40))
        self.center = ((WIDTH/2)*1.5, 30) #center location for status bar



class Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        topleft = ((WIDTH/2)*1.5)-150
        self.totalPoints = 0 #default value
        progressBar = pygame.Surface((self.totalPoints, 40)) #progress
        self.image = progressBar
        self.image.fill(foodColors[0])
        self.rect = pygame.Rect((topleft, 30),(300,40))
        self.center = ((WIDTH/2)*1.5, 30) #center location for status bar

    def addPoint(self, point):
        self.totalPoints += point
        if self.totalPoints> 300:
            self.levelup()
            self.update()
    
    def levelup(self):
        self.totalPoints = 0 #reset points to zero
        self.update()
        #do something with progress to update level?

    def update(self):
        progressBar = pygame.Surface((self.totalPoints, 40)) #progress
        self.image = progressBar
        self.image.fill(foodColors[0])


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # background
        self.ground_surf = backgroundImage.convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, player):

        self.center_target_camera(player)

        # ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)



def button(message, x, y, width, height, inactiveColor, activeColor, action=None):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse_x > x and y + height > mouse_y > y:
        pygame.draw.rect(screen, activeColor, (x, y, width, height))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, inactiveColor, (x, y, width, height))

    smallText = pygame.font.Font("playbuttonfont.ttf", 40)
    textSurf, textRect = text_objects(message, smallText)
    textRect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(textSurf, textRect)


def text_objects(text, font):
    textSurface = font.render(text, True, 'black')
    return textSurface, textSurface.get_rect()

def tutorial_loop():
        runTutorial = True
        finishTutorial = False
        blue = (0, 71, 171)
        green = (15, 82, 186)
        blue2 = (0, 150, 255)
        while runTutorial:


            for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                    runTutorial = False

            if finishTutorial == False:
                screen.fill('white')
                largeTexts = pygame.font.Font('titlefont.ttf', 165)
                TextSurf, TextRect = text_objects("E Colide", largeTexts)
                TextRect.center = ((WIDTH / 2), (HEIGHT / 8))
                screen.blit(TextSurf, TextRect)
                font1 = pygame.font.Font('freesansbold.ttf', 50)
                text2 = font1.render('Rules', True, blue)
                TextRect.center = ((WIDTH / 2) - 50 , ((HEIGHT / 3) + 45))
                screen.blit(text2, TextRect)

                font2 = pygame.font.Font('freesansbold.ttf', 25)

                line1 = font2.render('1) You are taking on the role of a bacteria! To move around the', True, green)
                TextRect.center = ((WIDTH / 2) - 25, ((HEIGHT / 3) + 125))
                screen.blit(line1, TextRect)

                line2 = font2.render('     grid, drag your mouse.', True, green)
                TextRect.center = ((WIDTH / 2)- 25, ((HEIGHT / 3) + 165))
                screen.blit(line2, TextRect)

                line3 = font2.render('2) Each round will last 3 minutes long. Time is indicated by the', True, green)
                TextRect.center = ((WIDTH / 2)- 25, ((HEIGHT / 3) + 235))
                screen.blit(line3, TextRect)

                line4 = font2.render('    timer in the top left corner.', True, green)
                TextRect.center = ((WIDTH / 2)- 25, ((HEIGHT / 3) + 275))
                screen.blit(line4, TextRect)

                line4 = font2.render('3) Absorb antidotes that are smaller to increase your mutation', True, green)
                TextRect.center = ((WIDTH / 2)- 25, ((HEIGHT / 3) + 345))
                screen.blit(line4, TextRect)

                line5 = font2.render('    counter! Absorbing bigger antidotes will decrease the', True, green)
                TextRect.center = ((WIDTH / 2)- 25, ((HEIGHT / 3) + 385))
                screen.blit(line5, TextRect)

                line6 = font2.render('    number of your mutations! ', True, green)
                TextRect.center = ((WIDTH / 2)- 25, ((HEIGHT / 3) + 425))
                screen.blit(line6, TextRect)

                line7 = font2.render('The objective of the game is to have the highest mutation', True, blue2)
                TextRect.center = ((WIDTH / 2)- 5, ((HEIGHT / 3) + 495))
                screen.blit(line7, TextRect)

                line8 = font2.render('counter possible!', True, blue2)
                TextRect.center = ((WIDTH / 2), ((HEIGHT / 3) + 535))
                screen.blit(line8, TextRect)

                pygame.display.update()

            else:
                print("gameover")
                screen.fill("RED")
                pygame.display.update()


def game_loop():
    startTime = pygame.time.get_ticks()
    minutes = 0
    seconds = 0
    timedLevel = 60000*3 # 3 minute
    running = True
    gameover = False
    bactPos = False

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if gameover == False:

            screen.fill('white')
            timer.tick(fps)
            mouse_x, mouse_y = pygame.mouse.get_pos()

            #countdown timer
            currentTime = pygame.time.get_ticks() # get current time

            # check if time limit has been reached
            if currentTime - startTime > timedLevel:
                gameover = True
                print("game over")
                #game_intro()
            else:
                # calculate time remaining
                time_remaining = timedLevel - (currentTime - startTime)
                minutes = int(time_remaining / 1000 / 60) # calculate minutes
                seconds = int(time_remaining / 1000 % 60) # calculate seconds

                # render time remaining on screen
                font = pygame.font.Font('Orbitron-Regular.ttf', 60)
                time = font.render("{}:{}".format(str(minutes).zfill(2), str(seconds).zfill(2)), True, foodColors[0])
                screen.blit(time, time.get_rect())

            """ if len(food_data) < 100:  # replenish food
                createFood_Data(food_data, random.randrange(150, 250))
                createFood_Obj(food_data, food_group, camera) """

            if len(antidote_group) < 10:  # replenish antidote enemies
                createAntidote_Data(antidote_data)
                createAntidote_Obj(antidote_data, antidote_group, camera)

            """ if len(mutation_data) < 10:  # replenish mutation enemies
                createMutation_Data(mutation_data, random.randrange(10, 20))
                createMutation_Obj(mutation_data, mutation_group, camera) """
            
            #check collision

            for antidote in antidote_group:
            # Check for collision between the Bacteria and the Antidote sprite
                if pygame.sprite.collide_rect(bacteria, antidote):
                    antidote.kill()
                    print(antidote.size)
                    break
            """
            if len(bacteriaAntidoteCollision) > 0:
                #collision found
                antidoteCollide = bacteriaAntidoteCollision[0]
                print('collision')
                print(type(antidoteCollide))
                if antidoteCollide.size > bacteriaSize:
                    
                    print(antidoteCollide.size)
                    #gameover = True
                    pass
                else:
                    antidoteSize = antidoteCollide.size
                    bacteria.eat(antidoteSize)
                    print("ate")
                    pass
            else:
                #print('0000')
                pass """
            
            #check_collision(bacteria,antidote_group)

            camera.update()
            camera.custom_draw(bacteria)
            all_sprites_list.update()
            all_sprites_list.draw(screen)
        else:
            print("gameover")
            screen.fill("RED")


#TODO: Add eating logic 1. Update score/progress bar 2. Increase bacteria size
        #update score
        score.addPoint(1)
        #update bacteria size

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if user hits red x button close window
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:  # if user hits a escape key close program
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.update()
        pygame.display.flip()



def game_intro():
    global buttonList
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill('white')
        largeText = pygame.font.Font('titlefont.ttf', 100)
        TextSurf, TextRect = text_objects("E Colide", largeText)
        TextRect.center = ((WIDTH / 2), (HEIGHT / 4))
        screen.blit(TextSurf, TextRect)

        buttonList = [
            button("PLAY", 340, 305, 220, 75, "yellow", "green", game_loop),
            button("RULES", 340, 420, 220, 75, "yellow", "green", tutorial_loop)
        ]

        pygame.display.update()
        timer.tick(15)



pygame.init()

all_sprites_list = pygame.sprite.Group()
bacteria = Bacteria()
all_sprites_list.add(bacteria)
food_group = pygame.sprite.Group()  # Define a sprite group ONLY for the food objects
antidote_group = pygame.sprite.Group()  # Define a sprite group ONLY for the antidote objects
mutation_group = pygame.sprite.Group()  # Define a sprite group ONLY for the mutation objects
camera = CameraGroup()
mutationCounter = 0
standardBarSprite = defaultBar()
all_sprites_list.add(standardBarSprite)
score = Score()
all_sprites_list.add(score)

# menu
game_intro()
# main loop
game_loop()
# quit
pygame.quit()

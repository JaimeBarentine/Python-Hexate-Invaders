import pygame

# used for randomness of velocity
import random



# the images
# remember to include with submission files!!!
playerShip = pygame.image.load('shipSmall.gif')
playerShip = pygame.transform.scale(playerShip, (60, 40))

playerShot = pygame.image.load('bullet.gif')
ufo = pygame.image.load('speaker.gif')
bomb = pygame.image.load('bomb.gif')
elephant = pygame.image.load('elephant.gif')
butterfly = pygame.image.load('butterfly.gif')

pygame.display.set_caption("Can you beat the high score?")

# global variables for cross use between classes
d = {'score' : 0, 'right' : True, 'up' : False, 'shot' : False, 'lives' : 3, 'hurt' : 0, 'difficulty' : False, 'hits' : 0, 'topShot' : False, 'bottomShot' : False, 'powerup' : 0}



# define all sprites to be rendered and put them in a group
all_sprites = pygame.sprite.Group()




# variables for the size of the screen
width = 700
height = 500
fps = 30

# colours for future reference
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)



#initialize the display
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))

# keeps the game running at a consistent frame rate
clock = pygame.time.Clock()


# the ship you play as
class Player(pygame.sprite.Sprite):

    
    #initiation of object specifities
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((50, 50))
        #self.image.fill(GREEN)
        self.image = playerShip
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        xVel = 5
        yVel = 5

# the velocity of the ship
    xVel = 5
    # max speed of ship
    speedMax = 15


# happens every frame
    def update(self):
        # checks to see if all shots are despawned when you have the powerup
        if d['powerup'] > 0:
            if diagShot1 not in all_sprites and diagShot2 not in all_sprites and bottomShot2 not in all_sprites and topShot2 not in all_sprites:
                d['shot'] = False
            else:
                d['shot'] = True
        else:
            if diagShot1 not in all_sprites:
                d['shot'] = False
        # for key presses
        keys = pygame.key.get_pressed()

        # change left and right momentum, slow the momentum to 0 if neither left or right keys are pressed
        if keys[pygame.K_RIGHT]:
            d['right'] = True
            if self.xVel < (self.speedMax + 0.1):
                self.xVel += 1
        elif keys[pygame.K_LEFT]:
            d['right'] = False
            if self.xVel > -(self.speedMax + 0.1):
                self.xVel -= 1
        else:
            if self.xVel > 1:
                self.xVel -= 0.5
            elif self.xVel < -1:
                self.xVel += 0.5
            else:
                self.xVel = 0

        #shoots up and down, spawning appropriate shot objects based on whether or not the player has the powerup
        if keys[pygame.K_UP]:
            d['up'] = False
            if d['shot'] == False:
                d['shot'] = True
                if d['powerup'] > 0:
                    all_sprites.add(diagShot2)
                    all_sprites.add(topShot2)
                all_sprites.add(diagShot1)

            
        elif keys[pygame.K_DOWN]:
            d['up'] = True
            if d['shot'] == False:
                d['shot'] = True
                if d['powerup'] > 0:
                    all_sprites.add(diagShot2)
                    all_sprites.add(bottomShot2)
                all_sprites.add(diagShot1)


                
        # change x position by momentum
        self.rect.x += self.xVel
        
        # wrap around when hitting the edge of the screen
        if self.rect.x > (width + 25):
            self.rect.x = -24
        
        if self.rect.x < -25:
            self.rect.x = (width + 24)


# the standard shot the player shoots
class diagonalShot(pygame.sprite.Sprite):

    #used to determine the direction the shot is facing upon instantiation
    direction = "topright"
    
    #initiation of object specificities
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerShot
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        
        
    startPos = False
    

# happens every frame
    def update(self):
        #print(random.randrange(1, 5))
        if self not in all_sprites and d['powerup'] == 0:
            #all_sprites.remove(self)
            d['shot'] = False
            self.startPos = False

        # for going back to normal right after the powerup timer reaches 0
        if d['powerup'] == 0 and (self.direction == "up" or self.direction == "down"):
            self.direction = "topright"

        # if first time running the update
        if self.startPos == False:

            # go to player coordinates
            self.rect.x = myPlayer.rect.x
            self.rect.y = myPlayer.rect.y

            # if player doesn't have powerup, set direction in whatever direction player wants to shoot
            if d['powerup'] == 0:
                if d['right'] == True:
                    if d['up'] == True:
                        self.direction = "topright"
                    else:
                        self.direction = "bottomright"
                else:
                    if d['up'] == True:
                        self.direction = "topleft"
                    else:
                        self.direction = "bottomleft"
            else:
                if d['up'] == True:
                    
                    self.direction = "up"
                else:
                    
                    self.direction = "down"
            # this is so the update doesn't run this if statement again
            self.startPos = True

        
        if d['powerup'] == 0:
        # sets which direction shot is facing
            if self.direction == "topright":
                self.rect.x += 15
                self.rect.y += 15
            elif self.direction == "bottomright":
                self.rect.x += 15
                self.rect.y -= 15
            elif self.direction == "bottomleft":
                self.rect.x -= 15
                self.rect.y -= 15
            elif self.direction == "topleft":
                self.rect.x -= 15
                self.rect.y += 15
        else:
            # for shot direction when player has the powerup
            if self == diagShot1:
                self.rect.x += 15
            elif self == diagShot2:
                self.rect.x -= 15
            
            if self.direction == "down":
                self.rect.y -= 15
            else:
                self.rect.y += 15


        # wrap around when hitting the left/right edge of the screen
        if self.rect.x > width:
            self.rect.x = 1
        
        if self.rect.x < 0:
            self.rect.x = (width - 1)

        #destroy self if too far up or down
        if self.rect.y > (height):
            all_sprites.remove(self)
            if d['powerup'] == False:
                d['shot'] = False
            self.startPos = False

        if self.rect.y < 0:
            all_sprites.remove(self)
            if d['powerup'] == False:
                d['shot'] = False
            self.startPos = False

        #check for collision
        for sprite in all_sprites:
            if sprite == self:
                continue
            if self.rect.colliderect(vertEnemy1.rect):
                #determine which direction ball should go based on point of collision
                #all_sprites.remove(self)
                #d['shot'] = False
                continue

# used for split shot, and it's what the NPCs use
class verticalShot(pygame.sprite.Sprite):

    # initiate object
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerShot
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.rect.x = width / 2
        self.rect.y = height / 2

    # used for going up or down
    direction = 0

    def update(self):
        
        if self not in all_sprites:
            self.direction = 0
            
        # sets direction to 0 if the shot it "cocked"
        if self == topShot1 and d['topShot'] == False:
            self.direction = 0
        if self == bottomShot1 and d['bottomShot'] == False:
            self.direction = 0

        # happens the first time the update runs it
        if self.direction == 0:
            #set starting position based on what object this is, be it an NPC or the player's split shot
            if self == topShot1:
                self.direction = 10
                
                if self == topShot1:
                    self.rect.x = topNPC.rect.x
                    self.rect.y = topNPC.rect.y
                    
                
            elif self == bottomShot1:
                self.direction = -10
                self.rect.x = bottomNPC.rect.x
                self.rect.y = bottomNPC.rect.y

            elif self == topShot2:
                self.direction = -15
                self.rect.x = myPlayer.rect.x
                self.rect.y = myPlayer.rect.y
            elif self == bottomShot2:
                self.direction = 15
                self.rect.x = myPlayer.rect.x
                self.rect.y = myPlayer.rect.y

        # change y position by direction variable
        self.rect.y += self.direction

        # despawns object and sets its variables back to default upon going off screen
        if self.rect.y > height or self.rect.y < 0:
            if self == topShot1:
                d['topShot'] = False
                self.direction = 0
                all_sprites.remove(topShot1)
                self.rect.x = topNPC.rect.x
                self.rect.y = topNPC.rect.y
            elif self == bottomShot1:
                d['bottomShot'] = False
                self.direcction = 0
                all_sprites.remove(bottomShot1)
                self.rect.x = bottomNPC.rect.x
                self.rect.y = bottomNPC.rect.y
            elif self == topShot2:
                self.direction = 0
                all_sprites.remove(topShot2)
                self.rect.x = myPlayer.rect.x
                self.rect.y = myPlayer.rect.y
            elif self == bottomShot2:
                self.direction = 0
                all_sprites.remove(bottomShot2)
                self.rect.x = myPlayer.rect.x
                self.rect.y = myPlayer.rect.y

        
            


# should be horizontalEnemy, but by the time I noticed I had already put a bunch of references to this class        
class verticalEnemy(pygame.sprite.Sprite):

    #initiate self
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ufo
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)

    # vars for movement direction and amount of time between firing bombs at the player
    direction = 0
    shotTimer = 90

    def update(self):
        # happens the first time the update runs
        if self.direction == 0:
            # rolls the dice to see if he'll start from the left and move right, or vice versa
            self.direction = random.randrange(1, 3)
            if self.direction == 1:
                self.rect.x = 0
                self.direction = 5
            else:
                self.rect.x = width
                self.direction = -5

        # if it's time to shoot, spawn its respective bomb and reset timer, else count timer down
        if self.shotTimer < 0:
            self.shotTimer = random.randrange(30, 90)
            if self == vertEnemy1:
                all_sprites.add(topBomb)
            else:
                all_sprites.add(bottomBomb)
        else:
            self.shotTimer -= 1

        # move x position by direction
        self.rect.x += self.direction
        #sets y position based on what object this is
        if self == vertEnemy1:
            self.rect.y = 25
            
        else:
            self.rect.y = (height - 100)
            
        # checks for collision of everything but its own rectangle
        for sprite in all_sprites:
            if sprite == self:
                continue
            if self.rect.colliderect(sprite.rect):
                if self in all_sprites:
                    # if hit by any of the player-friendly projectiles, destroy the projectile and add to the scrore, and remove self from all_sprites
                    if sprite == diagShot1 or sprite == topShot1 or sprite == bottomShot1 or sprite == topShot2 or sprite == bottomShot2 or sprite == diagShot2:
                        d['score'] += 10
                        d['hits'] += 1
                        self.direction = 0
                        self.shotTimer = random.randrange(30, 90)
                        all_sprites.remove(self)

                    # sets projectile specfic variables back to default
                    if sprite == diagShot1 and d['powerup'] == 0:
                        d['shot'] = False
                        all_sprites.remove(diagShot1)
                    elif sprite == topShot1:
                        d['topShot'] = False
                        all_sprites.remove(topShot1)
                    elif sprite == bottomShot1:
                        d['bottomShot'] = False
                        all_sprites.remove(bottomShot1)
                    elif sprite == topShot2:
                        all_sprites.remove(topShot2)
                    elif sprite == bottomShot2:
                        all_sprites.remove(bottomShot2)
                    
        # remove self if off screen or player loses a life
        if self.rect.x > width or self.rect.x < 0 or d['hurt'] > 0:
            self.direction = 0
            self.shotTimer = random.randrange(30, 90)
            all_sprites.remove(self)


# the vertical moving enemies that only appear when difficulty is on hard
class divingEnemy(pygame.sprite.Sprite):

    # initiate object
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ufo
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)

    #for determining movement direction
    direction = 0

    def update(self):
        # if first time
        if self.direction == 0:
            # roll the dice to determine if he'll start from the top and move down, or vice versa
            self.direction = random.randrange(1, 3)
            if self.direction == 1:
                self.direction = 5
                self.rect.y = -99
            else:
                self.direction = -5
                self.rect.y = (height + 99)
            self.rect.x = random.randrange(0, width)

        #change y position by direction
        self.rect.y += self.direction

        #detect collision for all object but myself
        for sprite in all_sprites:
            if sprite == self:
                continue
            if self.rect.colliderect(sprite.rect):
                # hurt player if that's what it hits
                if sprite == myPlayer:
                    if d['hurt'] == 0:
                        d['lives'] -= 1
                        d['hurt'] = 90
                        self.direction = 0

                # die if hit by projectile
                if sprite == diagShot1 or sprite == topShot1 or sprite == bottomShot1 or sprite == topShot2 or sprite == bottomShot2 or sprite == diagShot2:
                        d['score'] += 10
                        d['hits'] += 1
                        self.direction = 0
                        
                        all_sprites.remove(self)

                # deals with specificities of different projectiles based on if player has the powerup
                if (sprite == diagShot1) and (d['powerup'] == 0):
                    d['shot'] = False
                    all_sprites.remove(diagShot1)
                elif sprite == topShot1:
                    d['topShot'] = False
                    all_sprites.remove(topShot1)
                elif sprite == bottomShot1:
                    d['bottomShot'] = False
                    all_sprites.remove(bottomShot1)
                elif sprite == topShot2:
                    all_sprites.remove(topShot2)
                elif sprite == bottomShot2:
                    all_sprites.remove(bottomShot2)

        #remove self if off screen or player loses a life
        if self.rect.y > (height + 100) or self.rect.y < -100 or d['hurt'] > 0:
            self.direction = 0
            all_sprites.remove(self)
            


# the bomb projectile that enemies shoot at the player
class enemyShot(pygame.sprite.Sprite):

    #initiate self
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bomb
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)

    #used for movement direction
    direction = 0

    #happens every frame
    def update(self):
        #if first time
        if self.direction == 0:
            #sets initial position based on what object this is
            if self == topBomb:
                self.direction = 10
                self.rect.x = vertEnemy1.rect.x
                self.rect.y = 25
            else:
                self.direction = -10
                self.rect.x = vertEnemy2.rect.x
                self.rect.y = (height - 100)

        #changes y position by direction
        self.rect.y += self.direction

        #remove self if off screen or player loses a life
        if self.rect.y > width or self.rect.y < 0 or d['hurt'] > 0:
            self.direction = 0
            all_sprites.remove(self)

        #checks collision
        for sprite in all_sprites:
            if sprite == self:
                continue
            if self.rect.colliderect(sprite.rect):
                # if hit player, take a life
                if sprite == myPlayer:
                    if d['hurt'] == 0:
                        d['lives'] -= 1
                        d['hurt'] = 90
                # ignore if hitting a horizontal enemy
                if sprite == vertEnemy1 or sprite == vertEnemy2:
                    continue
                else:
                    self.direction = 0
                    all_sprites.remove(self)
                
            

# the elephant NPCs that shoot vertical shots for you if you shoot them
class NPC(pygame.sprite.Sprite):

    #initiate self
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = elephant
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)

    #used for movement direction
    movement = 0

    #happens every frame
    def update(self):

        #change x position by movement
        self.rect.x += self.movement

        #returns movement back to 0 over time
        if self.movement > 2:
            self.movement -= 1
        elif self.movement < -2:
            self.movement += 1
        else:
            self.movement = 0

        #wraps around the screen and adds momentum cause I got bored and wanted to have a little fun
        if self.rect.x > (width - 50):
            self.rect.x = 1
            self.movement += 10
        if self.rect.x < 0:
            self.rect.x = width - 51
            self.movement -= 10

        #sets y position based on which NPC this is
        if self == topNPC:
            self.rect.y = height - 200
        else:
            self.rect.y = 125

        #checks for collision
        for sprite in all_sprites:
            if sprite == self:
                continue
            if self.rect.colliderect(sprite.rect):

                # if hit by a player projectile
                if sprite == diagShot1 or sprite == diagShot2 or sprite == topShot2 or sprite == bottomShot2:
                    all_sprites.remove(sprite)

                    #shoot a friendly vertical shot in its respective direction at the enemies
                    if self == topNPC:
                        if d['topShot'] == False:
                            d['topShot'] = True
                            all_sprites.add(topShot1)
                            topShot1.direction = 0
                    else:
                        if d['bottomShot'] == False:
                            d['bottomShot'] = True
                            all_sprites.add(bottomShot1)
                            bottomShot1.direction = 0
                    d['shot'] = False
                    
                    #changes x momentum/movement depending on which side the NPC was hit
                    if sprite.rect.x > self.rect.x:
                        self.movement -= 10
                    else:
                        self.movement += 10


# the butter split shot powerup
class powerup(pygame.sprite.Sprite):

    #initiate self
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = butterfly
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)

    # for movement direction
    direction = 0

    #happens every frame
    def update(self):

        #if first time
        if self.direction == 0:
            #roll dice to see if powerup starts at top and moves down, or vice versa
            self.direction = random.randrange(1, 3)
            if self.direction == 1:
                self.direction = 5
                self.rect.y = 1
            else:
                self.direction = -5
                self.rect.y = (height + 100)
            self.rect.x = random.randrange(0, width)

        #changes y by direction
        self.rect.y += self.direction

        #checks for collision
        for sprite in all_sprites:
            if sprite == self:
                continue
            
            #if collides with player, start powerup timer
            if self.rect.colliderect(myPlayer.rect):
                d['powerup'] = 300
                all_sprites.remove(powerup)
                self.direction = 0

        #removes self if off screen
        if self.rect.y > height or self.rect.y < 0:
            all_sprites.remove(powerup)
            self.direction = 0
            



#for setting up text
display_surface = pygame.display.set_mode((width, height ))

#shared font for all text
font = pygame.font.Font('freesansbold.ttf', 32)
#score text
text = font.render('Score: ' + str(d['score']), True, GREEN, BLUE)
textRect = text.get_rect()
textRect.center = (width // 5, height // 15)
# lives text
text2 = font.render('Lives: ', True, WHITE, BLACK)
text2Rect = text2.get_rect()
text2Rect.center = (width // 5, height // 8)
#difficulty text
text3 = font.render('Work Please: ', True, WHITE, BLACK)
text3Rect = text3.get_rect()
text3Rect.center = (width // 1.3, height // 15)
#powerup timer text
text4 = font.render('Powerup timer: ', True, WHITE, BLACK)
text4Rect = text4.get_rect()
text4Rect.center = (width // 1.4, height // 7)


# define player and add it to all_sprites
myPlayer = Player()
all_sprites.add(myPlayer)

#defines player's default project, and the secondary projectile used when powerup timer is more than 0
diagShot1 = diagonalShot()
diagShot2 = diagonalShot()

#defines all possible enemy objects that can be on screen at any given time
vertEnemy1 = verticalEnemy()
vertEnemy2 = verticalEnemy()
diveBomb1 = divingEnemy()
diveBomb2 = divingEnemy()

#enemy's projectiles
topBomb = enemyShot()
bottomBomb = enemyShot()

#defines NPC objects
topNPC = NPC()
bottomNPC = NPC()

#all friendly vertical projectiles both from NPCs and powerup/split shot
topShot1 = verticalShot()
topShot2 = verticalShot()
bottomShot1 = verticalShot()
bottomShot2 = verticalShot()

#the powerup object
powerup = powerup()

#instantiates the NPCs
all_sprites.add(topNPC)
all_sprites.add(bottomNPC)

# timer for spawning multiple enemies, powerup, and difficulty
timer1 = random.randrange(30, 150)
timer2 = random.randrange(30, 150)
timer3 = random.randrange(30, 150)
timer4 = random.randrange(30, 150)
powerTimer = 120

difficultyCount = 20

#the game loop
running = True
while running:

    #counts down hurt timer for when player loses a life, no enemies can spawn in this period
    if d['hurt'] > 0:
        d['hurt'] -= 1
    else:
        d['hurt'] = 0

    if d['lives'] < 1:
        running = False

    #tracks how many enemies have been defeated to determine when difficulty should switch from easy to hard
    #switches to hard after 10 enemies are killed, then switches back to easy after 20
    #the easy mode always lasts 10 enemies, but hard mode adds 10 every time to its required kills to get back to easy
    if d['hits'] < 10:
        d['difficulty'] = False
        text3 = font.render('Difficulty: Easy', True, WHITE, BLACK)
    elif d['hits'] < difficultyCount:
        d['difficulty'] = True
        text3 = font.render('Difficulty: Hard', True, WHITE, BLACK)
    else:
        d['hits'] = 0
        difficultyCount += 10

    #updates text for score, lives, and powerup timer
    text2 = font.render('Lives: ' + str(d['lives']), True, WHITE, BLACK)
    text = font.render('Score: ' + str(d['score']), True, WHITE, BLACK)
    text4 = font.render('Powerup timer: ' + str(d['powerup']), True, WHITE, BLACK)

    #counts down time player has with the powerup
    if d['powerup'] > 1:
        d['powerup'] -= 1
        if d['powerup'] < 5:
            if diagShot1 in all_sprites:
                all_sprites.remove(diagShot1)
            if diagShot2 in all_sprites:
                all_sprites.remove(diagShot2)
            d['shot'] = False
    else:
        d['powerup'] = 0
    
    #keeps loop running at the right speed
    clock.tick(fps)

    #countdown timer for spawning this enemy
    if vertEnemy1 not in all_sprites:
        if timer1 < 0:
            timer1 = random.randrange(30, 150)
            all_sprites.add(vertEnemy1)
            
        else:
            timer1 -= 1

    #countdown timer for spawning this enemy
    if vertEnemy2 not in all_sprites:
        if timer2 < 0:
            timer2 = random.randrange(30, 150)
            all_sprites.add(vertEnemy2)
        else:
            timer2 -= 1

    #countdown timer for spawning this enemy
    if diveBomb1 not in all_sprites and d['difficulty'] == True:
        if timer3 < 0:
            timer3 = random.randrange(30, 150)
            all_sprites.add(diveBomb1)
        else:
            timer3 -= 1

    #countdown timer for spawning this enemy
    if diveBomb2 not in all_sprites and d['difficulty'] == True:
        if timer4 < 0:
            timer4 = random.randrange(30, 150)
            all_sprites.add(diveBomb2)
        else:
            timer4 -= 1

    #countdown timer for spawning powerup
    if powerup not in all_sprites and d['powerup'] == 0:
        if powerTimer < 0:
            powerTimer = random.randrange(90, 180)
            all_sprites.add(powerup)
        else:
            powerTimer -= 1
   

    #process input (events)
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False


    # update
    all_sprites.update()
    
    # Draw / render
    screen.fill(BLACK)
    display_surface.blit(text, textRect)
    display_surface.blit(text2, text2Rect)
    display_surface.blit(text3, text3Rect)
    display_surface.blit(text4, text4Rect)
    all_sprites.draw(screen)

    
    # flip the display
    pygame.display.flip()

#this is just the total screen, that way you can see your score before the window closes
while running == False:

    #just continues showing all game objects and ending text, so you can see how you died
    
    clock.tick(fps)
    text2 = font.render('Your final score was ' + str(d['score']), True, WHITE, BLACK)
    text = font.render('Game Over, spress space to end', True, WHITE, BLACK)
    keys = pygame.key.get_pressed()
    screen.fill(BLACK)
    display_surface.blit(text, textRect)
    display_surface.blit(text2, text2Rect)
    all_sprites.draw(screen)
    pygame.display.flip()
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = True

    #closes window when SPACE is pressed
    if keys[pygame.K_SPACE]:
        running = True  
    
    
            
pygame.quit()

import pygame, sys
from pygame.locals import *
import random, time

#Initialzing 
pygame.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SPEED_Coin = 5
SCORE_Enemy = 0
SCORE_Coin = 0
#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load(r"C:\Users\Sauka\OneDrive\Рабочий стол\Lab 8\Car\AnimatedStreet.png")

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")



class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load((r"C:\Users\Sauka\OneDrive\Рабочий стол\Lab 8\Car\Enemy.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)

      def move(self):
        global SCORE_Enemy
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            SCORE_Enemy += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load((r"C:\Users\Sauka\OneDrive\Рабочий стол\Lab 8\Car\Player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load((r"C:\Users\Sauka\OneDrive\Рабочий стол\Lab 8\Car\coin.png"))
        self.image = pygame.transform.scale(self.image, (30, 30)) 
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE_Coin
        global SPEED 
        coin_point = random.randrange(1, 4) #Giving random weights to coins
        self.rect.move_ip(0,SPEED_Coin)

        if pygame.sprite.spritecollide(P1, coins, True): #When coin is collected, coin disappears
            pygame.mixer.Sound(r"C:\Users\Sauka\OneDrive\Рабочий стол\Lab 8\Car\Coin.wav").play()        #and score is increased by 1 point
            SCORE_Coin += coin_point
            SPEED += 0.25
            new_coin = Coin()          #If coin is collected this code helps to create a new coin
            coins.add(new_coin)
            all_sprites.add(new_coin)
        
        if (self.rect.bottom > 600): #If coin isn't collected this code helps to create a new coin
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

#Setting up Sprites        
P1 = Player()
E1 = Enemy()
C1 = Coin()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#Loop
while True:
    #Cycles through all events occuring  

      for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.25      
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

   
      DISPLAYSURF.blit(background, (0,0)) #scoreboard of the cars passed 
      scores = font_small.render("Enemies Passed: " + str(SCORE_Enemy), True, BLACK)
      DISPLAYSURF.blit(scores, (10,10))

      score_surface = font_small.render("Coins: " + str(SCORE_Coin), True, BLACK) #scoreboard of the coins collected
      DISPLAYSURF.blit(score_surface, (SCREEN_WIDTH - 100, 10))

    
    #Moves and Re-draws all Sprites
      for entity in all_sprites:
            entity.move()
            DISPLAYSURF.blit(entity.image, entity.rect)
    
    #To be run if collision occurs between Player and Enemy
      if pygame.sprite.spritecollideany(P1, enemies):
            pygame.mixer.Sound(r"C:\Users\Sauka\OneDrive\Рабочий стол\Lab 8\Car\crash.wav").play()
            time.sleep(1)
                   
            DISPLAYSURF.fill(RED)
            DISPLAYSURF.blit(game_over, (30,250))
          
            pygame.display.update()
            for entity in all_sprites:
                  entity.kill() 
            time.sleep(2)
            pygame.quit()
            sys.exit()        
        
      pygame.display.update()
      FramePerSec.tick(FPS)
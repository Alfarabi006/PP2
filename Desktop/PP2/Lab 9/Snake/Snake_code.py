
from os import scandir
from select import select
import pygame
import random
import sys
from pygame.locals import *
import time
import threading

BLACK = (0, 0, 0)
LINE_COLOR = (50, 50, 50)
HEIGHT = 400
WIDTH = 400
SPEED = 5
BLOCK_SIZE = 20
MAX_LEVEL = 2
SCORE = 0
LEVEL = 1


class Point:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y


class Wall:
    def __init__(self, level):
        self.body = []
        level = level % MAX_LEVEL
        f = open(r"C:\Users\Sauka\OneDrive\Рабочий стол\Lab 8\Snake\levels\level{}.txt".format(level), "r")
        
        for y in range(0, HEIGHT//BLOCK_SIZE + 1):
            for x in range(0, WIDTH//BLOCK_SIZE + 1):
                if f.read(1) == '#':
                    self.body.append(Point(x, y))
        
    def draw(self):
        for point in self.body:
            rect = pygame.Rect(BLOCK_SIZE * point.x, BLOCK_SIZE * point.y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, (226, 135, 67), rect)


class Food:
    def __init__(self, wall):
        self.body = None
        self.wall = wall
        self.lock = threading.Lock()
        self.update_locationfirst()
        self.update_locationsecond()

    def update_locationfirst(self):
        self.lock.acquire()
        while True:
            self.body = Point(random.randint(0, WIDTH//BLOCK_SIZE-1), random.randint(0, HEIGHT//BLOCK_SIZE-1))
            if not any(point.x == self.body.x and point.y == self.body.y for point in self.wall.body):
                break 
        self.lock.release()
        self.timer = threading.Timer(random.randrange(5, 10), self.update_locationfirst)
        self.timer.start()

    def update_locationsecond(self):
        while True:
            self.body = Point(random.randint(0, WIDTH//BLOCK_SIZE-1), random.randint(0, HEIGHT//BLOCK_SIZE-1))
            if not any(point.x == self.body.x and point.y == self.body.y for point in self.wall.body):
                break
    
    def draw(self):
        rect = pygame.Rect(BLOCK_SIZE * self.body.x, BLOCK_SIZE * self.body.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, (0, 255, 0), rect)

    def move(self):
        self.update_locationsecond()

class Snake:
    def __init__(self):
        self.body = [Point(10, 11)]
        self.dx = 0
        self.dy = 0
        self.level = 0

    def game_over(self):
        font = pygame.font.SysFont("Verdana", 30)
        text = font.render("GAME OVER", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        SCREEN.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    def move(self, wall):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i-1].x
            self.body[i].y = self.body[i-1].y

        self.body[0].x += self.dx 
        self.body[0].y += self.dy 

        if self.body[0].x * BLOCK_SIZE > WIDTH:
            self.body[0].x = 0
    
        if self.body[0].y * BLOCK_SIZE > HEIGHT:
            self.body[0].y = 0

        if self.body[0].x < 0:
            self.body[0].x = WIDTH / BLOCK_SIZE
    
        if self.body[0].y < 0:
            self.body[0].y = HEIGHT / BLOCK_SIZE

        for point in wall.body:
            if self.body[0].x == point.x and self.body[0].y == point.y and not (self.body[0].x == 0 or self.body[0].y == 0 or self.body[0].x == WIDTH//BLOCK_SIZE or self.body[0].y == HEIGHT//BLOCK_SIZE):
                self.game_over()

    def draw(self):
        point = self.body[0]
        rect = pygame.Rect(BLOCK_SIZE * point.x, BLOCK_SIZE * point.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, (255, 0, 0), rect)

        for point in self.body[1:]:
            rect = pygame.Rect(BLOCK_SIZE * point.x, BLOCK_SIZE * point.y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, (0, 255, 0), rect)

    def check_collision(self, food):
        if self.body[0].x == food.body.x and self.body[0].y == food.body.y:
            food_score = random.randrange(1, 4)
            global SCORE
            SCORE += food_score
            food.move()
            self.body.insert(0, Point(self.body[0].x + self.dx, self.body[0].y + self.dy))

    def shorten(self):
        self.body.pop()

def main():
    global SCREEN, CLOCK, SPEED, LEVEL
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    font_small = pygame.font.SysFont("Verdana", 15)

    snake = Snake()
    wall = Wall(snake.level)
    food = Food(wall) 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.dx = 1
                    snake.dy = 0
                if event.key == pygame.K_LEFT:
                    snake.dx = -1
                    snake.dy = 0
                if event.key == pygame.K_UP:
                    snake.dx = 0
                    snake.dy = -1
                if event.key == pygame.K_DOWN:
                    snake.dx = 0
                    snake.dy = 1

        if len(snake.body) > 4 and len(snake.body) % 2 == 1:
            newLevel = snake.level + 1
            LEVEL += 1
            SPEED += 1 #Speed increases every level passed
            snake = Snake()
            snake.level = newLevel
            wall = Wall(snake.level)
            food = Food(wall) # pass new wall to Food object when the level changes

        
        snake.move(wall)
        food.lock.acquire()
        snake.check_collision(food)
        food.lock.release()
        SCREEN.fill(BLACK)
        wall.draw()
        food.draw()
        snake.draw()
        
        drawGrid()
        
        score_surface = font_small.render("SCORE: " + str(SCORE), True, (255, 255, 255)) #scoreboard of the foods eaten
        SCREEN.blit(score_surface, (315, 5))

        level_surface = font_small.render("Level: " + str(snake.level + 1), True, (255, 255, 255)) #scoreboard of the level
        SCREEN.blit(level_surface, (10, 5))
        
        pygame.display.update()
        CLOCK.tick(SPEED) #Speed becomes faster


def drawGrid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, LINE_COLOR, rect, 1)

main()

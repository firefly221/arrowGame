from math import *
import random
import pygame
import sys

pygame.init()


X = 960
Y = 960

screen = pygame.display.set_mode((X,Y))

clock = pygame.time.Clock()

pygame.display.flip()

class Grass:
    def __init__(self,x,y):
        self.block = pygame.image.load("grass.png")
        self.rect = self.block.get_rect()
        self.rect.topleft = (x,y)

    def draw(self,screen):
        screen.blit(self.block,self.rect)


class Wall:
    def __init__(self,x,y):
        self.block = pygame.image.load("bricksx64.png")
        self.rect = self.block.get_rect()
        self.rect.topleft =(x,y)

    def draw(self,screen):
        screen.blit(self.block,self.rect)



class Player:
    def __init__(self,x,y):
        self.block = pygame.image.load("czolg.png")
        self.block = pygame.transform.scale(self.block,(64,64))
        self.rect = self.block.get_rect()
        self.rect.topleft = (x,y)
        self.currX = x
        self.currY = y

    def draw(self,screen):
        screen.blit(self.block,self.rect)

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.centerx-=5
        elif key[pygame.K_RIGHT]:
            self.rect.centerx+=5
        elif key[pygame.K_UP]:
            self.rect.centery-=5
        elif key[pygame.K_DOWN]:
            self.rect.centery+=5
        



GAME_GRID_NUMS = []
GAME_GRID = []

for i in range(15):
    GAME_GRID_NUMS.append([])
    GAME_GRID.append([])
    for j in range(15):
        GAME_GRID_NUMS[-1].append(random.randint(0,4))
        GAME_GRID[-1].append(None)



for i in range(15):
    for j in range(15):
        if GAME_GRID_NUMS[i][j] != 0:
            GAME_GRID[i][j] = Grass(64*i,64*j)
        else:
            GAME_GRID[i][j] = Wall(64*i,64*j)


player1 = Player(64,64)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    for i in range(15):
        for j in range(15):
            GAME_GRID[i][j].draw(screen)
    player1.draw(screen)
    player1.move()


    clock.tick(60)
    pygame.display.update()
    screen.fill("black")












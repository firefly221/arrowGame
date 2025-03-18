import neat.population
import pygame
import neat
import time
import os
import random

pygame.font.init()


WIN_WIDTH = 500
WIN_HEIGHT = 800


ARROW_IMGS = [pygame.transform.scale2x(pygame.image.load('arrow.png'))]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load('imgs/pipe1.png'))
BASE_IMG = pygame.transform.scale2x(pygame.image.load('imgs/base1.png'))
BG_IMG = pygame.transform.scale2x(pygame.image.load('imgs/bg1.png'))

STAT_FONT = pygame.font.SysFont("comicsans",50)

WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))



class Arrow:

    IMGS = ARROW_IMGS
    
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0  
        self.t = 0
        self.vel = -5
        self.height = self.y
        self.img = self.IMGS[0]

    def change_dir(self):
        self.vel *= -1
        self.t = 0
        self.height = self.y


    def move(self):
        
        self.t += 1

        self.y = self.y + self.vel

        if self.vel < 0:
            self.tilt = 20
        else:
            self.tilt = -20

    def draw(self, win):   
        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self,x):
        self.x = x
        self.height = 0
        self.gap = 300

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG,False,True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(40,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL 
    
    def draw(self,win):
        
        win.blit(self.PIPE_TOP,(self.x,self.top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))
        
    def collide(self,arrow,win):
        arrow_mask = arrow.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - arrow.x,self.top - round(arrow.y))
        bottom_offset = (self.x - arrow.x,self.bottom - round(arrow.y))

        b_point = arrow_mask.overlap(bottom_mask,bottom_offset)
        t_point = arrow_mask.overlap(top_mask,top_offset)

        if t_point or b_point:
            return True

        return False


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))





def blitRotateCenter(surf, image, topleft, angle):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)



def draw_window(win,arrows,pipes,base,score):
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score:" + str(score),1,(255,255,255))
    win.blit(text,(WIN_WIDTH-10-text.get_width(),10))
    base.draw(win)
    for arrow in arrows:
        arrow.draw(win)
    pygame.display.update()


clock = pygame.time.Clock()


#Potrzebne parametry
def main(genomes,config):


    nets = []
    ge = []
    arrows = []

    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        arrows.append(Arrow(230,340))
        g.fitness = 0
        ge.append(g)

    base = Base(700)
    pipes = [Pipe(600)]
    score = 0
    add_pipe = False
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))



    while True:
        
        add_pipe = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pipe_id = 0
        if len(arrows) > 0:
            if len(pipes) > 1 and arrows[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_id = 1
        else:
            break

        for id,arrow in enumerate(arrows):
            arrow.move()
            ge[id].fitness += 0.1
            
            output = nets[id].activate((arrow.y,abs(arrow.y - pipes[pipe_id].height),abs(arrow.y - pipes[pipe_id].bottom)))

            if output[0] > 0.1:
                arrow.change_dir()

        rem = []
        for pipe in pipes:
            for id,arrow in enumerate(arrows):
                if pipe.collide(arrow,win):
                    ge[id].fitness-=1
                    arrows.pop(id)
                    nets.pop(id)
                    ge.pop(id)
                
                if not pipe.passed and pipe.x < arrow.x:
                    pipe.passed = True
                    add_pipe = True
                    score+=1
                pipe.move()

            if pipe.x + pipe.PIPE_BOTTOM.get_width() < 0:
                    rem.append(pipe)

        if add_pipe:
            pipes.append(Pipe(600))
            for g in ge:
                g.fitness+=5

        for pipe in rem:
            pipes.remove(pipe)

        for id,arrow in enumerate(arrows):
            if arrow.y + arrow.img.get_height() > 730 or arrow.y < 0:
                arrows.pop(id)
                nets.pop(id)
                ge.pop(id)

            

        base.move()
        keys = pygame.key.get_just_pressed()
        
        #Testowanie
        
        
        arrow.move()
        draw_window(win,arrows,pipes,base,score)
        clock.tick(40)





def run(config_dir):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         dir)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    #Daje przydatne info
    population.add_reporter(neat.StatisticsReporter())

    winner = population.run(main,50)



if __name__ == '__main__':
    dir = 'config.txt'
    run(dir)
    













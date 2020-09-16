import pygame
import math
import random


screen_width = 430
screen_height = 445


class Box:
    def __init__(self, color, pos):
        self.color = color
        if(color == 0):
            box_file = 'BoxRed.png'
        if(color == 1):
            box_file = 'BoxYellow.png'
        if(color == 2):
            box_file = 'BoxGreen.png'
        self.surface = pygame.image.load(box_file)
        self.pos = pos
        self.is_ok = True
        self.goal = False
        self.time_spent = 0
        self.xpos = 80 + (35 * (pos[0] - 2))
        self.ypos = 315

    def draw(self, screen):
        #screen.blit(self.surface, [80,315])
        screen.blit(self.surface, [self.xpos,self.ypos])
        #70 to move left to right or 35 for half slots
        #60 for up and down

    def update(self):
        self.time_spent += 1

    def check_offBelt(self):
        x = self.pos[0]
        y = self.pos[1]
        c = self.color
        if(((x < 2 or x > 8) and y < 4) or y < 1):
            self.is_ok = False
        if(x < 2 and y > 3 and c != 0):
            self.is_ok = False
        if(x > 2 and x < 8 and y > 5 and c != 1):
            self.is_ok = False
        if(x > 8 and y > 3 and c != 2):
            self.is_ok = False

    def check_goal(self):
        x = self.pos[0]
        y = self.pos[1]
        c = self.color
        if(x < 2 and y > 3 and c == 0):
            self.goal = True
        if(x > 2 and x < 8 and y > 5 and c == 1):
            self.goal = True
        if(x > 8 and y > 3 and c == 2):
            self.goal = True


class PyGame2D2:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.map = pygame.image.load('map.png')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 30)
        c = random.choice([0,1,2])
        self.box = Box(c, [random.choice([2,4,6,8]), 1,c])
        #self.game_speed = 4

    def action(self, action):
        if action == 0:
            self.box.pos[0] += 1
            self.box.pos[1] += 1
            self.box.xpos += 35
            self.box.ypos -= 60
        if action == 1:
            self.box.pos[0] += 2
            self.box.xpos += 70
        if action == 2:
            self.box.pos[0] += 1
            self.box.pos[1] -= 1
            self.box.xpos += 35
            self.box.ypos += 60
        if action == 3:
            self.box.pos[0] -= 1
            self.box.pos[1] -= 1
            self.box.xpos -= 35
            self.box.ypos += 60
        if action == 4:
            self.box.pos[0] -= 2
            self.box.xpos -= 70
        if action == 5:
            self.box.pos[0] -= 1
            self.box.pos[1] += 1
            self.box.xpos -= 35
            self.box.ypos -= 60

        self.box.update()
        self.box.check_offBelt()
        self.box.check_goal()

    def evaluate(self):
        reward = -1

        if not self.box.is_ok:
            reward -= 100

        elif self.box.goal:
            reward += 10

        return reward

    def is_done(self):
        if not self.box.is_ok or self.box.goal:
            #self.box.pos = [2, 1]
            return True
        return False

    def observe(self):
        return self.box.pos

    def view(self):
        # draw game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        self.screen.blit(self.map, (0, 0))
        self.box.draw(self.screen)
        pygame.display.update()
        #self.clock.tick(self.game_speed)
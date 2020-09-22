import pygame
import math
import random

# Main screen dimentions
screen_width = 430
screen_height = 445


class Box:
    # Initiating a box with pos[x,y,color]
    def __init__(self, pos):
        self.color = pos[2]
        # Choosing the box color
        if(self.color == 0):
            box_file = 'BoxRed.png'
        if(self.color == 1):
            box_file = 'BoxYellow.png'
        if(self.color == 2):
            box_file = 'BoxGreen.png'
        # Loading the chosen box file
        self.surface = pygame.image.load(box_file)
        self.pos = pos
        # If the box fell of the belt is set false
        self.is_ok = True
        # If the box reached the goal is set true
        self.goal = False
        # If the box got the reward is set true
        self.reward_given = False
        # Time spent by box on the belt
        self.time_spent = 0
        # Starting position of the box with a random X and a preset Y
        self.xpos = 80 + (35 * (pos[0] - 2))
        self.ypos = 315

    # Drawing the box on the screen
    def draw(self, screen):
        screen.blit(self.surface, [self.xpos, self.ypos])
        # 70 to move left to right or 35 for half slots
        # 60 for up and down

    # Updating the time spent after ever step
    def update(self):
        self.time_spent += 1

    # Checking if the box fell off the belt
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

    # Checking if the box reached the goal
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
    # Initiating the screen
    def __init__(self):
        pygame.init()
        # Creating the screen with given height and width
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        # Loading the belt file
        self.map = pygame.image.load('map.png')

        # Creating the boxes
        c = random.choice([0, 1, 2])
        l = [2, 4, 6, 8]
        x = random.choice(l)
        l.remove(x)
        self.box1 = Box([x, 1, c])
        c = random.choice([0, 1, 2])
        self.box2 = Box([random.choice(l), 1, c])
    # Picking an action

    def action(self, action):
        # Decoding the action back into two actions for each box
        l = decodeAction(action)

        # Moving box1 up-right
        if l[0] == 0 and not self.box1.reward_given:
            self.box1.pos[0] += 1
            self.box1.pos[1] += 1
            self.box1.xpos += 35
            self.box1.ypos -= 60
        # Moving box1 right
        if l[0] == 1 and not self.box1.reward_given:
            self.box1.pos[0] += 2
            self.box1.xpos += 70
        # Moving box1 down-right
        if l[0] == 2 and not self.box1.reward_given:
            self.box1.pos[0] += 1
            self.box1.pos[1] -= 1
            self.box1.xpos += 35
            self.box1.ypos += 60
        # Moving box1 down-left
        if l[0] == 3 and not self.box1.reward_given:
            self.box1.pos[0] -= 1
            self.box1.pos[1] -= 1
            self.box1.xpos -= 35
            self.box1.ypos += 60
        # Moving box1 left
        if l[0] == 4 and not self.box1.reward_given:
            self.box1.pos[0] -= 2
            self.box1.xpos -= 70
        # Moving box1 up-left
        if l[0] == 5 and not self.box1.reward_given:
            self.box1.pos[0] -= 1
            self.box1.pos[1] += 1
            self.box1.xpos -= 35
            self.box1.ypos -= 60

        # Moving box2 up-right
        if l[1] == 0 and not self.box2.reward_given:
            self.box2.pos[1] += 1
            self.box2.xpos += 35
            self.box2.pos[0] += 1
            self.box2.ypos -= 60
        # Moving box2 right
        if l[1] == 1 and not self.box2.reward_given:
            self.box2.pos[0] += 2
            self.box2.xpos += 70
        # Moving box2 down-right
        if l[1] == 2 and not self.box2.reward_given:
            self.box2.pos[0] += 1
            self.box2.pos[1] -= 1
            self.box2.xpos += 35
            self.box2.ypos += 60
        # Moving box2 down-left
        if l[1] == 3 and not self.box2.reward_given:
            self.box2.pos[0] -= 1
            self.box2.pos[1] -= 1
            self.box2.xpos -= 35
            self.box2.ypos += 60
        # Moving box2 left
        if l[1] == 4 and not self.box2.reward_given:
            self.box2.pos[0] -= 2
            self.box2.xpos -= 70
        # Moving box2 up-left
        if l[1] == 5 and not self.box2.reward_given:
            self.box2.pos[0] -= 1
            self.box2.pos[1] += 1
            self.box2.xpos -= 35
            self.box2.ypos -= 60

        # Updating the time spent and checking the boxes positions
        self.box1.update()
        self.box1.check_offBelt()
        self.box1.check_goal()

        self.box2.update()
        self.box2.check_offBelt()
        self.box2.check_goal()

    # Evaluating the rewards of the boxes
    def evaluate(self):
        reward = [0, 0]
        # Penalty of 10 with each step to find the goal faster
        if (not self.box1.reward_given):
            reward[0] -= 10
        if (not self.box2.reward_given):
            reward[1] -= 10

        # If box1 fall give penalty of 100
        if (not self.box1.is_ok) and (not self.box1.reward_given):
            reward[0] -= 100
            self.box1.reward_given = True
        # If box1 reach goal give reward of 1000
        elif self.box1.goal and (not self.box1.reward_given):
            reward[0] += 1000
            self.box1.reward_given = True
        # If box2 fall give penalty of 100
        if not self.box2.is_ok and (not self.box2.reward_given):
            reward[1] -= 100
            self.box2.reward_given = True
        # If box2 reach goal give reward of 1000
        elif self.box2.goal and (not self.box2.reward_given):
            reward[1] += 1000
            self.box2.reward_given = True

        return reward

    # Check if both boxes reached their goals
    def is_done(self):
        if (self.box1.reward_given and self.box2.reward_given):
            return True
        return False

    # Return the boxes positions
    def observe(self):
        return [self.box1.pos, self.box2.pos]

    # Draw the belt and boxes
    def view(self):
        # Draw game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        self.screen.blit(self.map, (0, 0))
        self.box1.draw(self.screen)
        self.box2.draw(self.screen)
        pygame.display.update()

# Decode action into an array with two integers representing actions for each box


def decodeAction(i):
    x = 0
    y = 0
    while(i >= 7):
        i -= 7
        x += 1
    while(i > 0):
        i -= 1
        y += 1
    return([x, y])

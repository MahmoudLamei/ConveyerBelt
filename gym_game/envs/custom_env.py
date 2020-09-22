import gym
from gym import spaces
import numpy as np
from gym_game.envs.pygame_2d import PyGame2D2


class CustomEnv(gym.Env):
    #metadata = {'render.modes' : ['human']}
    def __init__(self):
        self.pygame = PyGame2D2()
        # Discrete action space with the number of actions
        self.action_space = spaces.Discrete(6)
        # Observation space with the X and Y and their max valuse which are 10 and 6
        self.observation_space = spaces.Box(
            np.array([0, 0]), np.array([10, 6]), dtype=np.int)

    # Reseting the game
    def reset(self):
        del self.pygame
        self.pygame = PyGame2D2()
        obs = self.pygame.observe()
        return obs

    # Taking a step
    def step(self, action):
        # Take action
        self.pygame.action(action)
        # Observe position
        obs = self.pygame.observe()
        # Evaluate reward
        reward = self.pygame.evaluate()
        # Check if the episode is finished
        done = self.pygame.is_done()
        return obs, reward, done, {}

    # Draw the game
    def render(self, mode="human", close=False):
        self.pygame.view()

import gym
from gym import spaces
import pygame
import random
pygame.init()

class CustomEnv(gym.Env):
  """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self):
    super(CustomEnv, self).__init__()
    #left, right, left rotation, right rotation, hard drop, wait 
    self.action_space = spaces.Discrete(6)
    

    self.observation_space = [[0 for x in range(10)] for y in range(24)]

  def step(self, action):
    # Execute one time step within the environment
    ...
  def reset(self):
    # Reset the state of the environment to an initial state
    ...
  def render(self, mode='human', close=False):
    # Render the environment to the screen
    ...
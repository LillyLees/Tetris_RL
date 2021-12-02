import math
import random
import numpy as np
from collections import namedtuple, deque
from itertools import count
from PIL import Image

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward')) #represents a transition from state action, to next_state and reward 
class ReplayMemory():
    def __init__(self, size):
        self.memory = deque([],maxlen=size) #creating a memory que of our deffined size 
    
    def push(self, states):
        self.memory.append(Transition(states)) #save a certain transition in reply memory

    def sample(self, sample_size):
        return random.sample(self.memory, sample_size) #returns a random batch of memory of deffined sample size for tranining

    def current_len(self):
        return len(self.memory) #return the current size of reply memory



class NeuralNetwork(nn.Module):

    def __init__(self):
        super(NeuralNetwork, self).__init__()
#10 x 24 input image for conv1
        self.number_of_actions = 5 #5 diffrent options for output
        self.gamma = 0.99
        self.final_epsilon = 0.0001
        self.initial_epsilon = 1
        self.number_of_iterations = 2000000
        self.replay_memory_size = 10000
        self.minibatch_size = 32

        self.conv1 = nn.Conv2d(4, 32, 8, 4)
        self.relu1 = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(32, 64, 4, 2)
        self.relu2 = nn.ReLU(inplace=True)
        self.conv3 = nn.Conv2d(64, 64, 3, 1)
        self.relu3 = nn.ReLU(inplace=True)
        self.fc4 = nn.Linear(3136, 512)
        self.relu4 = nn.ReLU(inplace=True)
        self.fc5 = nn.Linear(512, self.number_of_actions)

    def forward(self, x): #N,C,H,W
        out = self.conv1(x)
        out = self.relu1(out)
        out = self.conv2(out)
        out = self.relu2(out)
        out = self.conv3(out)
        out = self.relu3(out)
        out = out.view(out.size()[0], -1)
        out = self.fc4(out)
        out = self.relu4(out)
        out = self.fc5(out)

        return out

class Actions(NeuralNetwork):
    def __init__(self):
        super().__init__()
        self.possible_moves = ["H","L","R","RL","RR"] #Hard drop, Left one, Right one, Left Rotation, Right Rotation
        self.total_moves = 0
        #self.eps = 1
        self.eps = 2
        self.state_action = []
        self.current_game_state = None
        
    def pick_random_move(self):
        moves = random.choice(self.possible_moves)
        return moves
    
    def get_action(self):
        ran = random.randint(0,100) / 100
        if ran < self.eps:
            return self.pick_random_move()
        else:
            return self.get_best_action()

    def update_eps(self):
        self.eps = 1 / self.total_moves 

    def get_best_action(self):
        pass

    def add_memory(self,current_state, next_state, reward, finished):

    






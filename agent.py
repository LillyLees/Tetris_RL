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



class DQN(nn.Module): #deep Q network class

    def __init__(self):
        super(DQN, self).__init__()
#10 x 24 input image for conv1
        self.number_of_actions = 5 #5 diffrent options for output
        self.gamma = 0.99
        self.final_epsilon = 0.0001
        self.initial_epsilon = 1
        self.number_of_iterations = 2000000
        self.replay_memory_size = 10000
        self.minibatch_size = 32

        self.conv1 = nn.Conv2d(1, 6, 10, 24)
        self.conv2 = nn.Conv2d(6, 16, 10, 24)
        self.fc1 = nn.Linear(16 * 10 * 24, 120)  
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, self.number_of_actions)

    def forward(self, x): 
        x = F.max_pool2d(F.relu(self.conv1(x)), (10, 24))
        x = torch.flatten(x, 1) 
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class Agent(DQN, ReplayMemory):
    def __init__(self):
        super().__init__()
        self.possible_moves = ["H","L","R","RL","RR"] #Hard drop, Left one, Right one, Left Rotation, Right Rotation
        self.total_moves = 0
        #self.eps = 1
        self.eps = 2
        self.current_state = []
        
        
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

    def update_current_state(self, current_tet, board, score):
        self.current_state.append(current_tet)
        self.current_state.append(board)
        self.current_state.append(score)


    






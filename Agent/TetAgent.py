import tqdm
import math
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count
from PIL import Image

import torch
import torch.nn as nn
from torch.nn.modules import flatten
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
from DeepQN import *
from ReplayMem import *

import sys

from Enviroment import *


#from Enviroment import *

env = CustomEnv()

is_ipython = 'inline' in matplotlib.get_backend()
if is_ipython:
    from IPython import display

plt.ion()

# if gpu is to be used
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
 

BATCH_SIZE = 128
GAMMA = 0.999
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 200
TARGET_UPDATE = 10

screen_height = env.board_height
screen_width = env.board_width

# Get number of actions from gym action space
n_actions = env.action_space.n

#policy_net = DQN().to(device) used to itnitalize NNs
#target_net = DQN().to(device)

policy_net = torch.load('nets/policy_net.ckpt')
target_net = torch.load('nets/target_net.ckpt')


optimizer = optim.RMSprop(policy_net.parameters())
memory = ReplayMemory(10000)


steps_done = 0

def ran_move():
    m = [0,1,1,1,2,2,2,3,3,4,5]
    return random.choice(m)

def select_action(state):
    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * \
        math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            return torch.argmax(policy_net(state), dim=1).item()
    else:
        return ran_move()


episode_durations = []

def optimize_model():
    print("optimizing")
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    batch = Transition(*zip(*transitions))
    
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.bool)
    
    non_final_next_pieces = torch.cat([torch.tensor([s[1]]).unsqueeze(0) for s in list(batch.next_state)
                                                if s is not None]).to(device).float() 
    
    non_final_next_board = torch.cat([torch.tensor([s[0]]) for s in list(batch.next_state)
                                                if s is not None]).squeeze(0).squeeze(0).float() 

    board_batch = torch.cat([torch.tensor([s[0]]) for s in batch.state]).squeeze(0).squeeze(0).float() 

    piece_batch = torch.cat([torch.tensor([s[1]]).unsqueeze(0) for s in batch.state]).to(device).float() 

    
    #embed board, emebed peice. cant cat because diffre number of dims. 
    action_batch = torch.cat([torch.tensor(s).unsqueeze(0) for s in batch.action]).to(device)
    reward_batch = torch.cat(batch.reward).to(device)

    state_action_values = policy_net((board_batch, piece_batch))#.gather(1, action_batch)  #THIS LINE KILL ME #issue
    
    

    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    next_state_values[non_final_mask] = target_net((non_final_next_board, non_final_next_pieces)).max(1)[0].detach()
    
    # Compute the expected Q values
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    # Compute Huber loss
    criterion = nn.SmoothL1Loss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

    # Optimize the model
    optimizer.zero_grad()
    loss.backward()
    for param in policy_net.parameters():
        param.grad.data.clamp_(-1, 1)
    optimizer.step()
    print(f'LOSS {loss}')
    
    return int(loss)

def plot(x,y):
    plt.scatter(x, y)
    plt.show()

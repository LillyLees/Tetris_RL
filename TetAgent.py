import gym
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
from Enviroment import *

env = CustomEnv()
#env.action_space.sample()

#env = gym.make('CartPole-v0').unwrapped

# set up matplotlib
is_ipython = 'inline' in matplotlib.get_backend()
if is_ipython:
    from IPython import display

plt.ion()

# if gpu is to be used
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([],maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

class DQN(nn.Module):

    def __init__(self):
        super(DQN, self).__init__()
        
        self.conv1_board = nn.Conv2d(1, 16, kernel_size=3, stride=1)
        self.conv2_board = nn.Conv2d(16, 32, kernel_size=3, stride=1)
        self.conv3_board = nn.Conv2d(32, 6, kernel_size=3, stride=1)


        
        self.fc1 = nn.Linear(433, 2048)
        self.fc2 = nn.Linear(2048, 6)
        

        self.flatten = nn.Flatten()

    def flt_totns(self, arr):
        flt = []
        for l in arr:
            flt.extend(l)
        return torch.tensor(flt).unsqueeze(0).unsqueeze(0).unsqueeze(0).to(device).float()

    def forward(self, states): #inputs to conv layers should be Tensors not list. convert list => tensor

        board, piece = states
        print(board)
        exit
        #board = self.flt_totns(board)
        #embed board 2
        embed_piece = torch.tensor(piece).unsqueeze(0).unsqueeze(0).to(device).float() #some reason getting diffrent dims
        #board = torch.FloatTensor(board).unsqueeze(0).unsqueeze(0).to(device)
        #print(embed_piece)
        if type(piece) == int:
            board = torch.FloatTensor(board).unsqueeze(0).unsqueeze(0).to(device) #issue
           # board = self.flt_totns(board) #breaks code, Kernal size to big (3x 3) 
            print(board.shape)
            embed_piece = torch.tensor(piece).unsqueeze(0).unsqueeze(0).to(device).float()
            
        embed_board = self.flatten(self.conv3_board(self.conv2_board(self.conv1_board(board))))
        
        if type(piece) != int:
            #print(f"BS {embed_board.shape}")
            #print(f"PS {piece}") #[[1],[2],[7].....] etc
            #print(f"EB {embed_board}")
            embed_piece = piece #[128, 1]
            
  
        #print(f"peice Shape: {embed_piece.shape}") 
        #print(f"Board Shape: {embed_board.shape}")
        #print(f"Peice {embed_piece}") #[[1],[2],[7].....] etc
        #print(f"board {embed_board}")

        embed_joined = torch.cat([embed_board, embed_piece],dim=1)
        #print(f"shape of both: {embed_joined.shape}") #[1,433] when playing this is ok
        # [1, 73712] when training and len of embed
        return torch.argmax(self.fc2(self.fc1(embed_joined)))
       

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

policy_net = DQN().to(device)
target_net = DQN().to(device)
#target_net.load_state_dict(policy_net.state_dict())
#target_net.eval()

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
            return policy_net(state).item()
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
    
    non_final_next_pieces = torch.cat([torch.tensor(s[1]).unsqueeze(0) for s in list(batch.next_state)
                                                if s is not None]).float()
    non_final_next_board = torch.cat([torch.tensor(s[0]) for s in list(batch.next_state)
                                                if s is not None]).float()

    board_batch = torch.cat([torch.tensor([s[0]]) for s in batch.state]).squeeze(0).squeeze(0).float() 
    #print("BBBBB", board_batch)
    #for s in batch.state:
    #    print(f"BS E {s[1]}")
    piece_batch = torch.cat([torch.tensor([s[1]]).unsqueeze(0) for s in batch.state]).to(device).float() 
    
    #piece_batch = piece_batch.permute(1, 0)
    
    #print(f"PB {piece_batch}")
    
    #embed board, emebed peice. cant cat because diffre number of dims. 
    action_batch = torch.cat([torch.tensor(s).unsqueeze(0) for s in batch.action]).to(device)
    reward_batch = torch.cat(batch.reward).to(device)

    #print(f"PB {piece_batch.shape}")
    #l = torch.cat([torch.tensor(policy_net((i,l))) for i, l in board_batch, piece_batch]).to(device).float().gather(1, action_batch)
    #for i, l in board_batch, piece_batch:
    #    policy_net((i,l)).gather(1, action_batch)

    state_action_values = policy_net((board_batch, piece_batch)).gather(1, action_batch) #THIS LINE KILL ME #issue

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



num_episodes = 100
for i_episode in range(num_episodes):
    # Initialize the environment and state
    env.reset()
    cur_tet, board = env.get_state()
    #state = [torch.FloatTensor(board), torch.FloatTensor(cur_tet)]
    state = [board, cur_tet]

    for t in tqdm.tqdm(range(100)):
        # Select and perform an action
        action = select_action(state)

        _, reward, playing, _ = env.step(action)
        reward = torch.tensor([reward], device=device)
        
        env.Render_m()
        time.sleep(0.1)
    
        if playing:
            cur_tet, board = env.get_state()
            next_state = [board, cur_tet]

        else:
            next_state = None

        # Store the transition in memory
        memory.push(state, action, next_state, reward)
        env.Render_m()
        # Move to the next state
        state = next_state

        # Perform one step of the optimization (on the policy network)
        
        if not playing:
            print(playing)
            episode_durations.append(t + 1)
            #plot_durations()
            break
        
        env.Render_m()
    # Update the target network, copying all weights and biases in DQN
    optimize_model()
    if i_episode % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())
    
print('Complete')
#env.render()
env.close()
'''plt.ioff()
plt.show()'''
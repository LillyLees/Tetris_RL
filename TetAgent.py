import gym
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
        
        
        self.conv1_board = nn.Conv2d(240, 16, kernel_size=5, stride=2)
        self.conv2_board = nn.Conv2d(16, 32, kernel_size=5, stride=2)
        self.conv3_board = nn.Conv2d(32, 6, kernel_size=5, stride=2)

        self.conv1_piece = nn.Conv2d(1, 16, kernel_size=5, stride=2)
        self.conv2_piece = nn.Conv2d(16, 6, kernel_size=5, stride=2)

        self.fc1 = nn.Linear(1, 32)
        self.fc2 = nn.Linear(32, 6)
        

        self.flatten = nn.Flatten()

    def flt(self, arr):
        flt = []
        for l in arr:
            flt.extend(l)
        return flt

    def forward(self, states): #inputs to conv layers should be Tensors not list. convert list => tensor 
        board, piece = states
        board = self.flt(board)
        embed_board = flatten(self.conv3_board(self.conv2_board(self.conv1_board(board))))
        embed_piece = flatten(self.conv2_piece(self.conv1_piece(piece)))
        embed_joined = torch.cat([embed_board, embed_piece])

        return self.fc2(self.fc1(embed_joined))

'''class DQN(nn.Module):

    def __init__(self, h, w, outputs):
        super(DQN, self).__init__()
        
        
        self.conv1 = nn.Conv2d(((10,24),1), 16, kernel_size=5, stride=2)
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=5, stride=2)
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(32, 32, kernel_size=5, stride=2)
        self.bn3 = nn.BatchNorm2d(32)

    
        def conv2d_size_out(size, kernel_size = 5, stride = 2):
            return (size - (kernel_size - 1) - 1) // stride  + 1

        convw = conv2d_size_out(conv2d_size_out(conv2d_size_out(w)))
        convh = conv2d_size_out(conv2d_size_out(conv2d_size_out(h)))
        linear_input_size = convw * convh * 32
        self.head = nn.Linear(linear_input_size, outputs)


    def forward(self, x):
        x = x.to(device)
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        return self.head(x.view(x.size(0), -1)) '''


env.reset()
'''plt.figure()
plt.imshow(get_screen().cpu().squeeze(0).permute(1, 2, 0).numpy(),
           interpolation='none')
plt.title('Example extracted screen')
plt.show()'''

BATCH_SIZE = 128
GAMMA = 0.999
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 200
TARGET_UPDATE = 10

# Get screen size so that we can initialize layers correctly based on shape
# returned from AI gym. Typical dimensions at this point are close to 3x40x90
# which is the result of a clamped and down-scaled render buffer in get_screen()
#init_screen = get_screen()
#_, _, screen_height, screen_width = init_screen.shape
screen_height = env.board_height
screen_width = env.board_width

# Get number of actions from gym action space
n_actions = env.action_space.n

#policy_net = DQN(24, 10, n_actions).to(device)
#target_net = DQN(24, 10, n_actions).to(device)

policy_net = DQN().to(device)
target_net = DQN().to(device)
#target_net.load_state_dict(policy_net.state_dict())
#target_net.eval()

optimizer = optim.RMSprop(policy_net.parameters())
memory = ReplayMemory(10000)


steps_done = 0

def ran_move():
    m = [0,1,1,1,1,1,2,2,2,2,2,3,3,4,4,5]
    return random.choice(m)

def select_action(state):
    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * \
        math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            # t.max(1) will return largest column value of each row.
            # second column on max result is index of where max element was
            # found, so we pick action with the larger expected reward.
            return policy_net(state).max(1)[1].view(1, 1)
    else:
        #return torch.tensor([[random.randrange(6)]], device=device, dtype=torch.long)
        return ran_move()


episode_durations = []

def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
    # detailed explanation). This converts batch-array of Transitions
    # to Transition of batch-arrays.
    batch = Transition(*zip(*transitions))

    # Compute a mask of non-final states and concatenate the batch elements
    # (a final state would've been the one after which simulation ended)
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)

    # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
    # columns of actions taken. These are the actions which would've been taken
    # for each batch state according to policy_net
    state_action_values = policy_net(state_batch).gather(1, action_batch)

    # Compute V(s_{t+1}) for all next states.
    # Expected values of actions for non_final_next_states are computed based
    # on the "older" target_net; selecting their best reward with max(1)[0].
    # This is merged based on the mask, such that we'll have either the expected
    # state value or 0 in case the state was final.
    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0].detach()
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

num_episodes = 50
for i_episode in range(num_episodes):
    # Initialize the environment and state
    env.reset()
    cur_tet, board = env.get_state()
    state = [board, cur_tet]

    for t in count():
        # Select and perform an action
        action = select_action(state)
        #_, reward, done, _ = env.step(action.item())
        _, reward, done, _ = env.step(action)
        reward = torch.tensor([reward], device=device)
        
        env.Render_m()
        # Observe new state
        #last_screen = current_screen
        #current_screen = get_screen()
        if not done:
            next_state = env.get_State()
        else:
            next_state = None

        # Store the transition in memory
        memory.push(state, action, next_state, reward)
        env.Render_m()
        # Move to the next state
        state = next_state

        # Perform one step of the optimization (on the policy network)
        optimize_model()
        if done:
            episode_durations.append(t + 1)
            #plot_durations()
            break
        
        env.Render_m()
    # Update the target network, copying all weights and biases in DQN
    if i_episode % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())

print('Complete')
#env.render()
env.close()
'''plt.ioff()
plt.show()'''
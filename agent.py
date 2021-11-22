import torch
import torch.nn as nn
import random

class NeuralNetwork(nn.Module):

    def __init__(self):
        super(NeuralNetwork, self).__init__()

        self.number_of_actions = 2
        self.gamma = 0.99
        self.final_epsilon = 0.0001
        self.initial_epsilon = 0.1
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

    def forward(self, x):
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
        self.possible_moves = ["H","L","R","LR","RR"] #Hard drop, Left one, Right one, Left Rotation, Right Rotation
        self.total_moves = 0
        self.eps = 1
        
    def pick_random_move(self):
        moves = []
        no_moves = random.randint(1,2)
        for move in range(no_moves):
            moves.append(random.choice(self.possible_moves))
        return(moves)
    
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
    





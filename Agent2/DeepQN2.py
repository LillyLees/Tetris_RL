import torch
import torch.nn as nn

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class DQN(nn.Module):

    def __init__(self):
        super(DQN, self).__init__()
        
        self.conv1_board = nn.Conv2d(1, 16, kernel_size=1, stride=1)
        torch.nn.init.xavier_uniform_(self.conv1_board.weight)
        self.conv2_board = nn.Conv2d(16, 32, kernel_size=1, stride=1)
        torch.nn.init.xavier_uniform_(self.conv2_board.weight)
        self.conv3_board = nn.Conv2d(32, 6, kernel_size=1, stride=1)
        torch.nn.init.xavier_uniform_(self.conv3_board.weight)

        self.fc1 = nn.Linear(241, 2048)
        torch.nn.init.xavier_uniform_(self.fc1.weight)
        self.fc2 = nn.Linear(2048, 6)
        torch.nn.init.xavier_uniform_(self.fc2.weight)

        self.flatten = nn.Flatten()

    def forward(self, states): #inputs to conv layers should be Tensors not list. convert list => tensor

        board, piece = states
       
        embed_piece = torch.tensor(piece).unsqueeze(0).unsqueeze(0).to(device).float() #some reason getting diffrent dims
        #board = torch.FloatTensor(board).unsqueeze(0).unsqueeze(0).to(device)
        #print(embed_piece)
        if type(piece) == int:
            board = torch.FloatTensor(board).unsqueeze(0).unsqueeze(0).to(device) #issue
           # board = self.flt_totns(board) #breaks code, Kernal size to big (3x 3) 
            
            embed_piece = torch.tensor(piece).unsqueeze(0).unsqueeze(0).to(device).float()
        else:
            board = board.unsqueeze(1).to(device)
            embed_piece = piece.to(device)

        embed_board = self.flatten(self.conv3_board(self.conv2_board(self.conv1_board(board))))

        embed_joined = torch.cat([embed_board, embed_piece],dim=1)
        return self.fc2(self.fc1(embed_joined))
       
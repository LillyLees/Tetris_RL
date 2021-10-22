import pygame
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
pygame.init()

class Tetramino():
    def __init__(self):
        self.x_move, self.y_move = [0,0]
        self.Tetraminos = {"I": {0 : [(3 , 3 ), (3 , 4 ), (3, 5 ), (3, 6 )], 
                                90 : [(2 , 5 ), (3 , 5 ), (4 , 5), (5 , 5)] },
                    "J": {0 :[(3 , 3 ), (3 , 4 ), (3, 5 ), (2 , 3 )],
                    90 : [(3 , 3 ), (3 , 4 ), (3, 5 ), (2 , 3 )], #not done
                    180 :[(3 , 3 ), (3 , 4 ), (3, 5 ), (2 , 3 )], # not done
                    270 :[(3 , 3 ), (3 , 4 ), (3, 5 ), (2 , 3 )]}, # not done
                    "L": {0 :[(3 , 3 ), (3 , 4 ), (3, 5 ), (2 , 3 )],
                    90 : [(3 , 3 ), (3 , 4 ), (3, 5 ), (2 , 3 )], #not done
                    180 :[(3 , 3 ), (3 , 4 ), (3, 5 ), (2 , 3 )], # not done
                    270 :[(3 , 3 ), (3 , 4 ), (3, 5 ), (2 , 3 )]}, #not
                    "T": {0 :[(3 , 3 ), (3 , 4 ), (3, 5 ), (2 , 3 )], #not done
                    90 : [(3 , 3 ), (3 , 4 ), (3, 5 ), (2 , 3 )], #not done
                    180 :[(3 , 3 ), (3 , 4 ), (3, 5 ), (2 , 3 )], # not done
                    270 :[(3 , 3 ), (3 , 4 ), (3, 5 ), (2 , 3 )]}, #not done
                    "O": {0 : [(2 , 4), (3 , 4), (3, 5), (2, 5)]}, 
                    "S": {0 : [(3 , 3 ), (3 , 4 ), (3, 5 ), (3, 6 )], #not done
                                90 : [(2 , 5 ), (3 , 5 ), (4 , 5), (5 , 5)] }, # not done
                    "Z": {0 : [(3 , 3 ), (3 , 4 ), (3, 5 ), (3, 6 )], #not done
                                90 : [(2 , 5 ), (3 , 5 ), (4 , 5), (5 , 5)] }} #not done
      
                         
        self.Bag = ["I", "L", "J", "T", "O", "S", "Z"]
        self.new_tet = random.choice(self.Bag)
        self.currenttet_nexttet = []
        self.current_tet = "I"

    def get_current_tet(self, roation):
            return self.Tetraminos[self.current_tet][roation]
        
    def testyyy(self):
            print("ahahaha this works")


class Tetris(Tetramino):
    def __init__(self):
        super(Tetris, self).__init__()
        self.total_lines_cleared = 0 #number in range 1-10
        self.playing = True
        self.level = 0
        self.score = 0
        self.score_multiplier = [40,100,300,1200]
        #The Tets spawn in a 2x4 area laying horazontally
        self.board_height = 506
        self.board_width = 222
        self.blockSize = 20 #20 scale factor for dimensions 
        self.board = []
        self.screen = pygame.display.set_mode([self.board_width, self.board_height])
       

    def Draw_board(self):
            self.screen = pygame.display.set_mode([self.board_width, self.board_height]) 
            pygame.display.set_caption("Reward-tris")
            self.screen.fill((255, 193, 202))
            for row in range(24):
                for column in range(10):
                    if self.board[row][column] != 1:
                        color = (0,0,0)
                    else:
                        color = (255,255,255)
                    self.fill_square(color,column,row)

    def fill_square(self,color,column,row):
        pygame.draw.rect(self.screen,
                        color,
                        [(2 + self.blockSize) * column + 2,
                        (2 + self.blockSize) * row + 2,
                        self.blockSize,
                        self.blockSize])
    
    def spawn_tet(self): #spawns the current tetramino at rotation 0
        blocks = self.get_current_tet(0)
        #blocks = self.Tetraminos[self.current_tet][0]
        for block in blocks:
            y, x = block
            self.board[y][x] = 2
            self.fill_square
            self.fill_square((23,75,43),x,y)
    
    def temp_tet_drop(self):
        
        blocks = self.get_current_tet(90)
        #blocks = self.Tetraminos[self.current_tet][0]
        for block in blocks:
            y, x = block
            self.board[y][x] = 2
            self.fill_square((23,75,43),x + 4 ,y + 17)

    def make_grid(self):
            self.board = [[0 for x in range(10)] for y in range(24)]


    def Pull_Bag(self):
            self.Current_Tet = random.choice(self.Bag)
            return(self.Current_Tet_type)
    def Create_Tet(self):
            self.Current_Tet_shape = self.Tetraminos[self.Current_Tet_type]
        
    def get_lines_cleared(self):
            #get lines cleared 
            #for line in board if line full lines cleared += 1
            pass
    def calculate_score(self,lines_cleared):
            #score += 40 + (lines_cleared + self.level) * self.score_multipler[lines_cleared + 1]
            pass
    def drop_tetramino(rotation,line):
            #drop self.tetramino wiith rotation at line 
            pass

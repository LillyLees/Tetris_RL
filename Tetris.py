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
        self.rotation = 0
        self.rotation_index = 0
        self.moved_x = 0
        self.moved_y = 0

    def get_current_tet_coords(self, roation): #given rotation gets the coordanats for drawing the current tet
            return self.Tetraminos[self.get_current_tet()][roation]

    def get_current_tet(self): #returns the name of the current tet
        return  self.currenttet_nexttet[0]
        
    def get_net_tet(self): #return name of next tet up
        return self.currenttet_nexttet[1]

    def generate_new_tet(self):
            if len(self.currenttet_nexttet) == 0: #if the game just started then fill the tet que
                self.currenttet_nexttet.append(random.choice(self.Bag))
                self.currenttet_nexttet.append(random.choice(self.Bag))
            else: #shift second tet to frist tet, generate new second tet
                self.currenttet_nexttet[0] = self.currenttet_nexttet[1]
                self.currenttet_nexttet[1] = self.currenttet_nexttet.append(random.choice(self.Bag))


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
        blocks = self.get_current_tet(self.rotation)
        #blocks = self.Tetraminos[self.current_tet][0]
        for block in blocks:
            y, x = block
            self.board[y][x] = 2
            self.fill_square
            self.fill_square((23,75,43),x,y)
    
    def tet_hard_drop(self):
        
        blocks = self.get_current_tet(self.rotation) #get coordanates of rotated tet
        hit = False
        temp_y = 0
        while hit == False:
            hit = self.check_collision(temp_y, self.x_move)
            if hit == True:
                hit == True
            else:
                self.y_move += 1
        self.y_move += temp_y  
        for block in blocks:
            y, x = block
            self.board[y][x] = 2
            self.fill_square((23,75,43),x + self.x_move ,y + self.y_move)

    def make_grid(self):
            self.board = [[0 for x in range(10)] for y in range(24)]

    def check_collision(self,y_add, x_add):
        blocks = self.get_current_tet(self.rotation)
        for block in blocks:
                y, x = block
                if self.board[y+ y_add][x+ x_add] == 1:
                    return True 
        return False

    def drop_down_one(self):
        if self.check_collision(1, self.x_move) == False:
            self.y_move += 1
    
    def left_one(self):
        if self.check_collision(self.y_move, -1) == False:
            self.x_move -= 1
    
    def right_one(self):
        if self.check_collision(self.y_move, 1) == False:
            self.x_move += 1

    def left_rotation(self):
        if self.current_tet == "O":
            self.rotation = 0
        elif self.current_tet in ["S","Z","I"]:
            r = [0,90]
            self.rotation_index -= 1
            self.rotation = r[self.rotation_index]
        else:
            r = [0, 90, 180, 270]
            self.rotation_index -= 1
            self.rotation = r[self.rotation_index]

    def right_rotation(self):
        if self.current_tet == "O":
            self.rotation = 0
        elif self.current_tet in ["S","Z","I"]:
            r = [0,90]
            if self.rotation_index == 1:
                self.rotation_index = 0
            else:
                self.rotation_index += 1
            self.rotation = r[self.rotation_index]
        else:
            r = [0, 90, 180, 270]
            if self.rotation_index == 3:
                self.rotation_index = 0
            else:
                self.rotation_index += 1
            self.rotation = r[self.rotation_index]

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

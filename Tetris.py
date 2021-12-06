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
        self.Tetraminos = {"I": {0 : [[2 , 3 ], [2 , 4 ], [2, 5 ], [2, 6 ]], 
                                90 : [[0 , 5 ], [1 , 5 ], [2 , 5], [3 , 5]] },

                    "J": {0 :[[1 , 3 ], [1 , 4 ], [1, 5 ], [2 , 5 ]], 
                    90 : [[0 , 4 ], [1 , 4 ], [2, 4 ], [2 , 3 ]], 
                    180 :[[1 , 3 ], [2 , 4 ], [2, 5 ], [2 , 3 ]], 
                    270 :[[0 , 4 ], [1 , 4 ], [2, 4 ], [0 , 5 ]]}, 

                    "L": {0 :[[1 , 3 ], [1 , 4 ], [1, 5 ], [2 , 3 ]], 
                    90 : [[0 , 3 ], [1 , 4 ], [2, 4 ], [0 , 4]], 
                    180 :[[1 , 5 ], [2 , 4 ], [2, 5 ], [2 , 3 ]], 
                    270 :[[0 , 4 ], [1 , 4 ], [2, 4 ], [2 , 5 ]]},

                    "T": {0 :[[1 , 3 ], [1 , 4 ], [1, 5 ], [2 , 4 ]], 
                    90 : [[0 , 4 ], [1 , 4 ],[1, 3], [2 , 4 ]], 
                    180 :[[2 , 3 ], [2 , 4 ],[2, 5 ], [1 , 4 ]], 
                    270 :[[0 , 4 ], [1 , 4 ],[1, 5 ], [2 , 4]]}, 

                    "O": {0 : [[1 , 4], [2 , 4], [2, 5], [1, 5]]}, 

                    "S": {0 : [[1 , 5], [1 , 4],[2, 3 ], [2 , 4]], 
                        90 : [[0 , 3 ], [1 , 3 ],[1, 5 ], [2 , 4 ]] }, 

                    "Z": {0 : [[1 , 3 ], [1, 4],[2, 4 ], [2 , 5]], 
                                90 : [[0 , 5 ], [1 , 5],[1, 4 ], [2 , 4 ]] }} 
      
                         
        self.Bag = ["I", "L", "J", "T", "O", "S", "Z"]
        self.new_tet = random.choice(self.Bag)
        self.currenttet_nexttet = []
        self.current_tet = ""
        self.rotation = 0
        self.rotation_index = 0
        self.moved_x = 0
        self.moved_y = -1
        self.temp_y_move = 0
        self.dropped = False
        self.temp_index = 0

    def reset_tet(self):
        self.dropped = False
        self.x_move = 0
        self.y_move = -1
        self.temp_y_move = 0
        self.temp_index = 0
        self.rotation = 0
        self.rotation_index = 0
        self.generate_new_tet()
        self.current_tet = self.get_current_tet()

    def get_current_tet_coords(self, roation): #given rotation gets the coordanats for drawing the current tet
            return self.Tetraminos[self.currenttet_nexttet[0]][roation]
            

    def get_current_tet(self): #returns the name of the current tet
        return self.currenttet_nexttet[0]
        
    def get_net_tet(self): #return name of next tet up
        return self.currenttet_nexttet[1]

    def generate_new_tet(self):
            if len(self.currenttet_nexttet) == 0: #if the game just started then fill the tet que
                self.currenttet_nexttet.append(random.choice(self.Bag))
                self.currenttet_nexttet.append(random.choice(self.Bag))
            else: #shift second tet to frist tet, generate new second tet
                self.currenttet_nexttet[0] = self.currenttet_nexttet[1]
                self.currenttet_nexttet[1] = random.choice(self.Bag)
            self.current_tet = self.currenttet_nexttet[0]


class Tetris(Tetramino):
    def __init__(self):
        super(Tetris, self).__init__()
        self.total_lines_cleared = 0 #number in range 1-10
        self.playing = True
        self.level = 0
        self.score = 0
        self.temp_score = 0
        self.score_multiplier = [40,100,300,1200]
        #The Tets spawn in a 2x4 area laying horazontally
        self.board_height = 535
        self.board_width = 300
        self.blockSize = 20 #20 scale factor for dimensions 
        self.bit_map = []
        self.screen = pygame.display.set_mode([self.board_width, self.board_height])
        self.last_move = ""
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)

    def Draw_board(self):
            self.screen = pygame.display.set_mode([self.board_width, self.board_height]) 
            pygame.display.set_caption("Reward-tris")
            self.screen.fill((255, 193, 202))

            score_surface = self.myfont.render(str(self.score), True, (0, 0, 0))
            self.screen.blit(score_surface,(230,10))

            level_surface = self.myfont.render(str(self.level), True, (0, 0, 0))
            self.screen.blit(level_surface,(230,40))


            for row in range(0,24):
                for column in range(0,10):
                    if self.bit_map[row][column] == 0:
                        color = (0,0,0)
                    elif self.bit_map[row][column] == 2:
                        color = (24,255,35)
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
        blocks = self.get_current_tet_coords(self.rotation)
        for block in blocks:
            y, x = block
            self.bit_map[y + self.y_move][x] = 2
            self.fill_square
            self.fill_square((23,75,43),x,y + self.y_move)
    
    def tet_hard_drop(self):
        hit = False
        temp_y = -1
        while hit == False:
            temp_y += 1
            hit = self.check_collision(temp_y + 1, 0, self.rotation)
            
        self.y_move += temp_y
        self.temp_y_move = temp_y  
        self.dropped = True

    def make_bit_map(self):
            self.bit_map = [[0 for x in range(10)] for y in range(24)]

    def check_collision(self,y_add, x_add, rotation):
        blocks = self.get_current_tet_coords(rotation)
        for block in blocks:
                y, x = block
                if y + self.y_move + y_add > 23:
                    return True
                elif x + self.x_move + x_add > 9:
                    return True
                elif self.bit_map[y+ self.y_move + y_add][x+ self.x_move +x_add] == 1:
                    return True
                
        return False

    def drop_down_one(self):
        if self.check_collision(1, 0, self.rotation) == False:
            self.y_move += 1
        if self.check_collision(1, 0, self.rotation) == True:
            self.dropped = True
    
    def left_one(self):
        if self.check_collision(0, -1, self.rotation) == False:
            self.x_move -= 1
        if self.check_collision(1, 0, self.rotation) == True:
            self.dropped = True
    
    def right_one(self):
        if self.check_collision(0, 1, self.rotation) == False:
            self.x_move += 1
        if self.check_collision(1, 0, self.rotation) == True:
            self.dropped = True

    def left_rotation(self): #add check if collision 
        self.temp_index = self.rotation_index
        if self.current_tet == "O":
            self.rotation = 0
        else:
            if self.current_tet in ["S","Z","I"]:
                r = [0,90]
                self.temp_index -= 1
                TR = r[self.temp_index]
            else:
                r = [0, 90, 180, 270]
                self.temp_index -= 1
                TR = r[self.temp_index]
            if self.check_collision(0, 0, TR) == False:
                self.rotation = TR
                if self.check_collision(1, 0, self.rotation) == True:
                    self.dropped = True
                    self.rotation_index = self.temp_index

    def right_rotation(self): 
        self.temp_index = self.rotation_index
        if self.current_tet == "O":
            self.rotation = 0
        else:
            if self.current_tet in ["S","Z","I"]:
                r = [0,90]
                if self.rotation_index == 1:
                    self.temp_index = 0
                else:
                    self.temp_index += 1
                TR = r[self.temp_index]
            else:
                r = [0, 90, 180, 270]
                if self.rotation_index == 3:
                    TR = 0
                else:
                    self.temp_index += 1
                TR = r[self.temp_index]

            if self.check_collision(0, 0, TR) == False:
                self.rotation = TR
                if self.check_collision(1, 0, self.rotation) == True:
                    self.dropped = True
                    self.rotation_index = self.temp_index

    def Pull_Bag(self):
            self.Current_Tet = random.choice(self.Bag)
            return(self.Current_Tet_type)
    def Create_Tet(self):
            self.Current_Tet_shape = self.Tetraminos[self.Current_Tet_type]
 
    def clear_line(self):
        lines_cleared = 0
        row_number = -1
        for row in self.bit_map:
            row_number += 1
            if 0 not in row:
                lines_cleared += 1
                if row_number != 0:
                    self.bit_map[row_number] = self.bit_map[row_number - 1]
                self.bit_map[0] = [0 for x in range(10)]
        
        self.calculate_score(lines_cleared)
        self.total_lines_cleared += lines_cleared

        if self.total_lines_cleared > 9:
            self.update_level()
        
                
    def calculate_score(self,lines_cleared):
            scores = [40, 100, 300, 1200]
            if lines_cleared > 0:
                self.score += scores[lines_cleared - 1] * (self.level + 1)
            if self.last_move == "HD":
                self.score += 2 * self.temp_y_move
                self.score += self.y_move - self.temp_y_move
            else:
                self.score += self.y_move
            
    
    def update_level(self):
        if self.total_lines_cleared >= 10:
            self.level += 1
            self.total_lines_cleared = self.total_lines_cleared - 10 
    
    def place_tet(self):
        blocks = self.get_current_tet_coords(self.rotation)
        for block in blocks:
                y, x = block
                y += self.y_move
                x += self.x_move
                self.bit_map[y][x] = 1 
    
    def update_tet_position(self):
        blocks = self.get_current_tet_coords(self.rotation)
        for block in blocks:
                y, x = block
                y += self.y_move
                x += self.x_move
                self.bit_map[y][x] = 2
    
    def wipe_old_tet_position(self):
        for row in range(len(self.bit_map)):
            for square in range(10):
                if self.bit_map[row][square] == 2:
                    self.bit_map[row][square] = 0
    
    def redraw_board(self):
        self.wipe_old_tet_position()
        self.update_tet_position()
        self.Draw_board()

    def check_game_end(self):
        if 1 in self.bit_map[0]:
            self.playing = False
            return False
    
    def reward(self):
        return self.score - self.temp_score
    
    def game_states(self):
        return [self.current_tet, self.bit_map, self.score]

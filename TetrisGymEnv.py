import gym
from gym import spaces
import pygame
import random
pygame.init()

class Tetramino():
    def __init__(self):
        self.x_move, self.y_move = [0,0]
        self.Tetraminos = {"I": {0 : [[2 , 3 ], [2 , 4 ], [2, 5 ], [2, 6 ]], 
                                90 : [[0 , 5 ], [1 , 5 ], [2 , 5], [3 , 5]],
                                180 : [[2 , 3 ], [2 , 4 ], [2, 5 ], [2, 6 ]], 
                                270 : [[0 , 5 ], [1 , 5 ], [2 , 5], [3 , 5]]  },

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
                    270 :[[0 , 4 ], [1 , 4 ],[1, 5 ], [1 , 3]]}, 

                    "O": {0 : [[1 , 4], [2 , 4], [2, 5], [1, 5]]}, 

                    "S": {0 : [[1 , 5], [1 , 4],[2, 3 ], [2 , 4]], 
                        90 : [[0 , 4 ], [1 , 4 ],[1, 5 ], [2 , 5 ]],
                        180 : [[1 , 5], [1 , 4],[2, 3 ], [2 , 4]], 
                        270 : [[0 , 4 ], [1 , 4 ],[1, 5 ], [2 , 5 ]]}, 

                    "Z": {0 : [[1 , 3 ], [1, 4],[2, 4 ], [2 , 5]], 
                                90 : [[0 , 5 ], [1 , 5],[1, 4 ], [2 , 4 ]],
                                180 : [[1 , 3 ], [1, 4],[2, 4 ], [2 , 5]], 
                                270 : [[0 , 5 ], [1 , 5],[1, 4 ], [2 , 4 ]] }} 
      
                         
        self.Bag = ["I", "L", "J", "T", "O", "S", "Z"]
        self.current_tet = random.choice(self.Bag)
        self.rotations = [0, 90, 180, 270]
        self.rotation = 0

        self.rotation_index = 0
        self.moved_x = 0
        self.moved_y = -1
        self.temp_y_move = 0
        self.dropped = False
        

    def reset_tet(self):
        self.x_move, self.y_move = [0,0]
        self.rotation = 0
        self.rotation_index = 0
        self.moved_x = 0
        self.moved_y = -1
        self.temp_y_move = 0
        self.dropped = False
        

    def get_current_tet_coords(self, roation): #given rotation gets the coordanats for drawing the current tet
            return self.Tetraminos[self.currenttet_nexttet[0]][roation]
            
    def generate_new_tet(self):
            self.current_tet = random.choice(self.Bag)


class CustomEnv(gym.Env, Tetramino):
  """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self):
    super(CustomEnv, self).__init__()
    #left, right, left rotation, right rotation, hard drop, wait 
    self.action_space = spaces.Discrete(6)
    self.state = [[0 for x in range(10)] for y in range(24)]

    self.Bag = ["I", "L", "J", "T", "O", "S", "Z"]
    self.current_Tet = random.choice(self.Bag)

    self.drop_time = 0
    self.rows_dropped_tr = 0
    self.total_lines_cleared = 0 #number in range 1-10

    self.playing = True
    self.level = 0
    self.score = 0
    #self.temp_score = 0
    self.score_multiplier = [40,100,300,1200]
        #The Tets spawn in a 2x4 area laying horazontally
    self.board_height = 535
    self.board_width = 300
    self.blockSize = 20 #20 scale factor for dimensions 
    self.screen = pygame.display.set_mode([self.board_width, self.board_height])
    self.last_move = ""
    self.myfont = pygame.font.SysFont('Comic Sans MS', 30)

  def step(self, action):
    self.last_move = action
    movement_dict = {0 : self.tet_hard_drop, 1 : self.left_one, 2 : self.right_one, 
            3 : self.left_rotation, 4 : self.right_rotation, 5 : self.wait}
    movement_dict[action](action)
    reward = 0

    if self.dropped == True:
        self.place_tet()
    else:
        self.update_state()
    
    self.clear_line()
    self.update_level()
    reward = self.calculate_score()
    
    if 1 in self.state[0]:
        self.playing = False
        reward = -1

    return [self.state, reward, self.playing]

  def reset(self):
    # Reset the state of the environment to an initial state
    ...
  def render(self, mode='human', close=False):
    # Render the environment to the screen
    ...

  def reward(self):
        return self.score - self.temp_score
  
  
  def check_collision(self, y_add, x_add, rotation):
        blocks = self.get_current_tet_coords(rotation)
        for block in blocks:
                y, x = block
                y += self.y_move
                x += self.x_move

                if y + y_add > 23:
                    return True
                elif x + x_add > 9:
                    return True
                elif self.bit_map[y + y_add][x + x_add] == 1:
                    return True
                
        return False
  
  def wait(self):
      pass
  
  def tet_hard_drop(self):
        hit = False
        temp_y = -1
        while hit == False:
            temp_y += 1
            hit = self.check_collision(temp_y + 1, 0, self.rotation)
            
        self.y_move += temp_y
        self.temp_y_move = temp_y
        self.rows_dropped_tr = temp_y
        self.dropped = True


  def drop_down_one(self):
        if self.check_collision(1, 0, self.rotation) == False:
            self.y_move += 1
            self.rows_dropped_tr = 1
        else:
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

  def right_rotation(self):
      self.rotation(self, 1)
  
  def left_rotation(self):
      self.rotation(self, -1)

  def rotation(self, dir): 
        if self.current_tet == "O":
            self.rotation = 0
        else:
            if self.rotation == 3 and dir == 1:
                dir = -1
            elif self.rotation == -4 and dir == -1:
                dir = 3
            else:
                dir = self.rotation + dir
            temp_rot = self.rotations[dir]

            is_col = self.check_collision(0, 0, temp_rot)

            if is_col == False:
                self.rotation = dir
                is_col = self.check_collision(0, 1, temp_rot)
                if is_col == True:
                    self.dropped = True
  
  def place_tet(self):
        self.wipe_old_tet_position()
        blocks = self.get_current_tet_coords(self.rotation)
        for block in blocks:
                y, x = block
                y += self.y_move
                x += self.x_move
                self.bit_map[y][x] = 1 
    
  def update_state(self):
        self.wipe_old_tet_position()
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
            te = 0
            if lines_cleared > 0:
                self.score += scores[lines_cleared - 1] * (self.level + 1)
                te += scores[lines_cleared - 1] * (self.level + 1)
            if self.last_move == 0:
                self.score += 2 * self.rows_dropped_tr
                self.score += self.rows_dropped_tr
                te += 2 * self.rows_dropped_tr
                te += self.rows_dropped_tr
            else:
                self.score += self.rows_dropped_tr
                te += self.rows_dropped_tr
            
            return te
            
    
  def update_level(self):
        if self.total_lines_cleared >= 10:
            self.level += 1
            self.total_lines_cleared = self.total_lines_cleared - 10 


            
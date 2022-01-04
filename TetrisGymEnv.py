import gym
from gym import spaces
import pygame
import random
pygame.init()
import time 

class Tetramino():
    def __init__(self):
        self.x_move, self.y_move = [0,-1]
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
        self.rotation_index = 0
        self.rotation = self.rotations[self.rotation_index]
        self.temp_y_move = 0
        self.dropped = False
        

    def reset_tet(self):
        self.x_move, self.y_move = [0,-1]
        self.rotation_index = 0
        self.temp_y_move = 0
        self.dropped = False
        self.current_tet = random.choice(self.Bag)
        

    def get_current_tet_coords(self, roation): #given rotation gets the coordanats for drawing the current tet
            return self.Tetraminos[self.current_tet][roation]
            
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

    #self.Bag = ["I", "L", "J", "T", "O", "S", "Z"]
    #self.current_Tet = random.choice(self.Bag)

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

    self.movement_dict = {0 : self.tet_hard_drop, 1 : self.left_one, 2 : self.right_one, 
            3 : self.left_rotation, 4 : self.right_rotation, 5 : self.wait}

  def reset(self):
      self.reset_tet()
      self.last_move = ""
      self.playing = True
      self.level = 0
      self.score = 0
      self.drop_time = 0
      self.rows_dropped_tr = 0
      self.total_lines_cleared = 0
      self.state = [[0 for x in range(10)] for y in range(24)]

  def step(self, action):
    self.drop_time += 1
    self.last_move = action
    
    reward = 0

    if self.drop_time == 6:
        self.drop_down_one()
        self.drop_time = 0
    
    if self.dropped == True: #if enviro makes choice for agent agent's choice is ignored
        self.place_tet()
        
    else:
        self.movement_dict[action]()
        if self.dropped == True:
            self.place_tet()
        else:
            self.update_state()
    
    lc = self.clear_line()
    self.update_level()
    self.get_score(lc, action)
    reward = self.calc_reward(lc)

    if 1 in self.state[0]:
        self.playing = False
        reward = - reward
    
    if self.dropped == True:
        self.reset_tet()
        self.spawn_tet()

    return [self.state, reward, self.playing]

    
  def Render_m(self):
            self.screen = pygame.display.set_mode([self.board_width, self.board_height]) 
            pygame.display.set_caption("Reward-tris")
            self.screen.fill((255,255,255))

            score_surface = self.myfont.render(str(self.score), True, (0, 0, 0))
            self.screen.blit(score_surface,(230,10))

            level_surface = self.myfont.render(str(self.level), True, (0, 0, 0))
            self.screen.blit(level_surface,(230,40))


            for row in range(0,24):
                for column in range(0,10):
                    if self.state[row][column] == 0: #is an empty square
                        color = (200,200,200)
                    elif self.state[row][column] == 2: #has a falling block
                        color = (138,99,80)
                    else:
                        color = (255,191,212) #has a placed block
                    self.draw_square(color,column,row)
            
            pygame.display.flip()
  #close function

  def draw_square(self,color,column,row):
        pygame.draw.rect(self.screen,
                        color,
                        [(2 + self.blockSize) * column + 2,
                        (2 + self.blockSize) * row + 2,
                        self.blockSize,
                        self.blockSize])

  def calc_reward(self, lc): #score is proportional to the level and the lines cleared
        reward = 0
        ah = 0
        hol = 0
        for column in range(10): # calculates the aggragte height of each column, to be minamizd 
            h = 24
            for row in range(24):
                if self.state[row][column] == 0:
                    h -= 1
                else:
                    ah += h
                    break
        for column in range(10): # calculates the number of holes in the board
            h = 0
            on_col = False
            for row in range(24):
                if self.state[row][column] != 0:
                    on_col = True
                if on_col == True and self.state[row][column] == 0:
                    h += 1
            hol += h 
        reward = (-0.510066 * ah) + (-0.35663 * hol) + (0.760666 * lc) 
        return reward

        
  
  def spawn_tet(self): #spawns the current tetramino at rotation 0
        blocks = self.get_current_tet_coords(self.rotation)
        for block in blocks:
            y, x = block
            self.state[y + self.y_move][x] = 2
  
  def check_collision(self, y_add, x_add, rotation):
        blocks = self.get_current_tet_coords(rotation)
        for block in blocks:
                y, x = block
                y += self.y_move
                x += self.x_move

                if y + y_add > 23 or y + y_add < 0:
                    return True
                elif x + x_add > 9 or x + x_add < 0:
                    return True
                elif self.state[y + y_add][x + x_add] == 1:
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
        ("DP")
        if self.check_collision(1, 0, self.rotation) == False:
            self.y_move += 1
            self.rows_dropped_tr = 1
        else:
            self.dropped = True
    
  def left_one(self):
        print("LP")
        if self.check_collision(0, -1, self.rotation) == False:
            self.x_move -= 1
        if self.check_collision(1, 0, self.rotation) == True:
            self.dropped = True
    
  def right_one(self):
        print("RP")
        if self.check_collision(0, 1, self.rotation) == False:
            self.x_move += 1
        if self.check_collision(1, 0, self.rotation) == True:
            self.dropped = True

  def right_rotation(self):
      self.rotate(1)
  
  def left_rotation(self):
      self.rotate(-1)

  def rotate(self, dir): 
        if self.current_tet == "O":
            self.rotation_index = 0
        else:
            if self.rotation_index == 3 and dir == 1:
                dir = -1
            elif self.rotation_index == -4 and dir == -1:
                dir = 3
            else:
                dir = self.rotation_index + dir
            temp_rot = self.rotations[dir]

            is_col = self.check_collision(0, 0, temp_rot)

            if is_col == False:
                self.rotation_index = dir
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
                self.state[y][x] = 1 
    
  def update_state(self):
        self.wipe_old_tet_position()
        blocks = self.get_current_tet_coords(self.rotation)
        for block in blocks:
                y, x = block
                y += self.y_move
                x += self.x_move
                self.state[y][x] = 2
  
  def wipe_old_tet_position(self):
        for row in range(len(self.state)):
            for square in range(10):
                if self.state[row][square] == 2:
                    self.state[row][square] = 0

  def clear_line(self):
        lines_cleared = 0
        row_number = -1
        for row in self.state:
            row_number += 1
            if 0 not in row:
                lines_cleared += 1
                if row_number != 0:
                    self.state[row_number] = self.state[row_number - 1]
                self.state[0] = [0 for x in range(10)]
        
        #self.calculate_score(lines_cleared)
        self.total_lines_cleared += lines_cleared

        if self.total_lines_cleared > 9:
            self.update_level()
        return(lines_cleared)

                
  def get_score(self, lines_cleared, action):
            scores = [40, 100, 300, 1200]
          
            if lines_cleared > 0:
                print("pop")
                self.score += scores[lines_cleared - 1] * (self.level + 1)
                
            if action == 0:
                self.score += 2 * self.rows_dropped_tr
                self.score += self.rows_dropped_tr
                
            else:
                self.score += self.rows_dropped_tr
            
    
  def update_level(self):
        if self.total_lines_cleared >= 10:
            self.level += 1
            self.total_lines_cleared = self.total_lines_cleared - 10 

e = CustomEnv()

while e.playing == True:
    e.step(random.randint(0,5))
    e.Render_m()
    
    #for i in e.state:
    #    print(i)
    time.sleep(0.25) 
    #print("=====")


            
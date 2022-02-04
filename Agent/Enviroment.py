import gym
from gym import spaces
import pygame
pygame.init()


from Tetramino import *



class CustomEnv(gym.Env, Tetramino):
  """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self):
    super(CustomEnv, self).__init__()
    #left, right, left rotation, right rotation, hard drop, wait 
    self.action_space = spaces.Discrete(6)
    self.observation_space = [[0 for x in range(10)] for y in range(24)]

    self.drop_time = 0
    self.rows_dropped_tr = 0
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
      self.observation_space = [[0 for x in range(10)] for y in range(24)]
      self.temp_score = 0
  
  def get_state(self):
      return self.current_tet, self.observation_space
      
  def step(self, action):
    self.drop_time += 1
    self.last_move = action
    
    reward = 0

    if self.drop_time == 6:
        self.drop_down_one()
        self.drop_time = 0
    
    if self.dropped == True: #if enviro makes choice for agent agent's choice is ignored
        lc = self.place_tet()
        #lc = self.clear_line()
        #self.get_score(lc, action)
        
    else:
        self.movement_dict[action]()
        if self.dropped == True:
           lc =  self.place_tet()
            #lc = self.clear_line()
            #self.get_score(lc, action)
        else:
            self.update_state()
            lc = 0
    
    #lc = self.clear_line()
    #self.update_level()
    
    reward = self.calc_reward(lc)

    if self.check_game_end() == False:  
        self.playing = False
        reward = - reward
    
    if self.dropped == True:
        self.reset_tet()
        self.spawn_tet()
    
    info = {}

    return (self.observation_space, self.current_tet), reward, self.playing, info


  def check_game_end(self):
      if 1 in self.observation_space[0]:
          return False
      blocks = self.get_current_tet_coords(self.rotation)
      for block in blocks:
          y, x = block
          if self.observation_space[y][x] == 1:
              return False
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
                    if self.observation_space[row][column] == 0: #is an empty square
                        color = (200,200,200)
                    elif self.observation_space[row][column] == 2: #has a falling block
                        color = (138,99,80)
                    else:
                        color = (255,191,212) #has a placed block
                    self.draw_square(color,column,row)
            
            pygame.display.flip()
  
  def close(self):
      pygame.quit()

  def draw_square(self,color,column,row):
        pygame.draw.rect(self.screen,
                        color,
                        [(2 + self.blockSize) * column + 2,
                        (2 + self.blockSize) * row + 2,
                        self.blockSize,
                        self.blockSize])

  def calc_reward(self, lc): #score is proportional to the level and the lines cleared
        reward = 0
        ah = 24 #aggragate height, default is 24
        hol = 0 #holiness
        mh = 0 #max height
        in_dz = 0 #how many placed bloxs in danger zone (top three lines)
        bump = 0 #bumpyness (diff between each row)
        last_h = 0

        for column in range(10): # calculates the aggragte height of each column, to be minamizd 
            temp_mh = 0
            found_col = False #tower hasnt started yet

            for row in range(24):
                if self.observation_space[row][column] == 0:
                    ah -= 1
                    if found_col == True:
                        hol += 1 #if there is an empty space in a column

                if self.observation_space[row][column] == 1 and temp_mh == 0: #regiters height of column when it it found
                    temp_mh = 24 - row

                if self.observation_space[row][column] != 0: #pops when tower starts
                    found_col = True

            if column == 0:
                last_h = temp_mh

            bump += abs(temp_mh - last_h)
            last_h = temp_mh

            if temp_mh > mh:
                mh = temp_mh

        for row in range(3): #checking how many placed bloks in danger zone
            for blk in self.observation_space[row]:
                if blk == 1:
                    in_dz += 1

        #reward = (-0.55 * ah) + (-0.4 * hol) + (-0.7 * mh) + (-0.35 * bump) + (-3 * in_dz) + (0.1 * self.temp_score) + (2 * lc)
        reward = (0.76 *lc) + (-0.37 * hol) + (-0.18 * bump) + (-0.51 * ah)
        return reward

        
  
  def spawn_tet(self): #spawns the current tetramino at rotation 0
        blocks = self.get_current_tet_coords(self.rotation)
        for block in blocks:
            y, x = block
            self.observation_space[y + self.y_move][x] = 2
  
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
                elif self.observation_space[y + y_add][x + x_add] == 1:
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
        #print("Drop down one")
        if self.check_collision(1, 0, self.rotation) == False:
            self.y_move += 1
            self.rows_dropped_tr = 1
        else:
            self.dropped = True
    
  def left_one(self):
        #print("left one")
        if self.check_collision(0, -1, self.rotation) == False:
            self.x_move -= 1
        if self.check_collision(1, 0, self.rotation) == True:
            self.dropped = True
    
  def right_one(self):
        #print("right one")
        if self.check_collision(0, 1, self.rotation) == False:
            self.x_move += 1
        if self.check_collision(1, 0, self.rotation) == True:
            self.dropped = True

  def right_rotation(self):
      #print("right rotation")
      self.rotate(1)
  
  def left_rotation(self):
      #print("left rotation")
      self.rotate(-1)

  def rotate(self, dir): 
        if self.current_tet == 4:
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
                
                self.rotation = temp_rot
                self.rotation_index = dir
                is_col = self.check_collision(1, 0, temp_rot)
                if is_col == True:
                    self.dropped = True
  
  def place_tet(self):
        self.temp_score = 0
        blocks = self.get_current_tet_coords(self.rotation)
        for block in blocks:
                y, x = block
                y += self.y_move
                x += self.x_move
                self.observation_space[y][x] = 1
        lc = self.clear_line()
        self.get_score(lc, self.last_move)
        self.wipe_old_tet_position()
        return lc
    
  def update_state(self):
        self.wipe_old_tet_position()
        blocks = self.get_current_tet_coords(self.rotation)
        for block in blocks:
                y, x = block
                y += self.y_move
                x += self.x_move
                self.observation_space[y][x] = 2
  
  def wipe_old_tet_position(self):
        for row in range(len(self.observation_space)):
            for square in range(10):
                if self.observation_space[row][square] == 2:
                    self.observation_space[row][square] = 0

  def clear_line(self):
        lines_cleared = 0
        row_number = -1
        for row in self.observation_space:
            row_number += 1
            if 0 not in row:
                lines_cleared += 1
                if row_number != 0:
                    self.observation_space[row_number] = self.observation_space[row_number - 1]
                self.observation_space[0] = [0 for x in range(10)]
        
        #self.calculate_score(lines_cleared)
        self.total_lines_cleared += lines_cleared

        if self.total_lines_cleared > 9:
            self.update_level()
        return(lines_cleared)

                
  def get_score(self, lines_cleared, action):
            scores = [40, 100, 300, 1200]
          
            if lines_cleared > 0:
                self.temp_score += scores[lines_cleared - 1] * (self.level + 1)
                
            if action == 0:
                self.temp_score += 2 * self.rows_dropped_tr
                self.temp_score += self.rows_dropped_tr
                
            else:
                self.temp_score   += self.rows_dropped_tr
            self.score += self.temp_score   
    
  def update_level(self):
        if self.total_lines_cleared >= 10:
            self.level += 1
            self.total_lines_cleared = self.total_lines_cleared - 10 

env = CustomEnv()



            
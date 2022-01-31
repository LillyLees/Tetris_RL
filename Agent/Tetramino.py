from tabnanny import check
import gym
from gym import spaces
import pygame
import random
pygame.init()
import time 

class Tetramino():
    def __init__(self):
        self.x_move, self.y_move = [0,-1]
        self.Tetraminos = {0: {0 : [[3 , 3], [3 , 4 ], [3, 5 ], [3, 6 ]], #I
                                90 : [[1 , 5 ], [2 , 5 ], [3 , 5], [4 , 5]],
                                180 : [[3 , 3 ], [3 , 4 ], [3, 5 ], [3, 6 ]], 
                                270 : [[1 , 5 ], [2 , 5 ], [3 , 5], [4 , 5]]  },

                    2: {0 :[[2 , 3 ], [2 , 4 ], [2, 5 ], [3 , 5 ]], #J
                    90 : [[1 , 4 ], [2 , 4 ], [3, 4 ], [3 , 3 ]], 
                    180 :[[2 , 3 ], [3 , 4 ], [3, 5 ], [3 , 3 ]], 
                    270 :[[1 , 4 ], [2 , 4 ], [3, 4 ], [3 , 3 ]]}, 

                    1: {0 :[[2 , 3 ], [2 , 4 ], [2, 5 ], [3 , 3 ]], #L
                    90 : [[1 , 3 ], [2 , 4 ], [3, 4 ], [1 , 4]], 
                    180 :[[2 , 5 ], [3 , 4 ], [3, 5 ], [3 , 3 ]], 
                    270 :[[1 , 4 ], [2 , 4 ], [3, 4 ], [3 , 5 ]]},

                    3: {0 :[[2 , 3 ], [2 , 4 ], [2, 5 ], [3 , 4 ]], #T
                    90 : [[1 , 4 ], [2 , 4 ],[2, 3], [3 , 4 ]], 
                    180 :[[3 , 3 ], [3 , 4 ],[3, 5 ], [2 , 4 ]], 
                    270 :[[1 , 4 ], [2 , 4 ],[2, 5 ], [2 , 3]]}, 

                    4: {0 : [[2 , 4], [3 , 4], [3, 5], [2, 5]],
                    90 : [[2 , 4], [3 , 4], [3, 5], [2, 5]],
                    180 : [[2 , 4], [3 , 4], [3, 5], [2, 5]],
                    270 : [[2 , 4], [3 , 4], [3, 5], [2, 5]]}, #0

                    5: {0 : [[2 , 5], [2 , 4],[3, 3 ], [3 , 4]], #S
                        90 : [[1 , 4 ], [2 , 4 ],[2, 5 ], [3 , 5 ]],
                        180 : [[2 , 5], [2 , 4],[3, 3 ], [3 , 4]], 
                        270 : [[1 , 4 ], [2 , 4 ],[2, 5 ], [3 , 5 ]]}, 

                    6: {0 : [[2 , 3 ], [2, 4],[3, 4 ], [3 , 5]], #Z
                                90 : [[1, 5 ], [2 , 5],[2, 4 ], [3 , 4 ]],
                                180 : [[2 , 3 ], [2, 4],[3, 4 ], [3 , 5]], 
                                270 : [[1 , 5 ], [2 , 5],[2, 4 ], [3 , 4 ]] }} 
      
                         
        #self.Bag = ["I", "L", "J", "T", "O", "S", "Z"] 
        self.current_tet = random.randint(0,6) #I,L,J,T,O,S,Z
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
        self.current_tet = random.randint(0,6)
        

    def get_current_tet_coords(self, roation): #given rotation gets the coordanats for drawing the current tet
            
            return self.Tetraminos[self.current_tet][roation]
            
    def generate_new_tet(self):
            self.current_tet = random.randint(0,6)
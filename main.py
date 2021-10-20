import numpy as np
import pygame
from numpy import array
from Tetris import Tetris



Game = Tetris()

new_game = Tetris()
new_game.make_grid()
while new_game.playing == True:
    
    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            print("aaaaaa") 
            new_game.playing = False  
    new_game.Draw_board()
    new_game.spawn_tet()
    pygame.display.flip()

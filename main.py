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
            new_game.playing = False 
    move = [] #array of two moves 
    #possible moves: 
    #H hard drop
    #L left one
    #R right one
    #RL rotate left
    #RR rotate right 
    if move == "H":
        new_game.tet_hard_drop()
    new_game.Draw_board()
    new_game.spawn_tet()
    if new_game.dropped == True:
        new_game.reset_tet()

    pygame.display.flip()
    #get state, reward, done, action

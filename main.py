import numpy as np
import pygame
from numpy import array, left_shift
from Tetris import Tetris

Game = Tetris()
new_game = Tetris()
new_game.make_bit_map()
new_game.generate_new_tet()
new_game.spawn_tet()

while new_game.playing == True:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            new_game.playing = False
    
    moves = [] #array of two moves 
    
    new_game.generate_new_tet() #update tetramino que, if this is the first run itnitlize que with tets
    new_game.Draw_board() # draw current board states, if this is the first run this will be a new peice spawn

    for move in moves:
        new_game.get_move(move) #loop through each move and make the required changed to the bitmap
    new_game.update_tet_position()

    '''if new_game.dropped == True:
        new_game.place_tet()
        new_game.clear_line()  #check if there are any lines cleared, if there are this method also adds to the score and calcualtes a new level
        new_game.reset_tet()
        new_game.spawn_tet()
    
    new_game.redraw_board()
     #redraw board with new moves 
    new_game.check_game_end() '''
    pygame.display.flip()
    #get state, reward, done, action

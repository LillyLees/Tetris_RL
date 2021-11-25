import numpy as np
import pygame
from numpy import array, left_shift
from Tetris import Tetris
import time

from agent import Actions

Game = Tetris()
Agent = Actions()
new_game = Tetris()

new_game.make_bit_map()
new_game.generate_new_tet()
new_game.spawn_tet()
pygame.font.init()

turns = 5

movement_dict = {"H" : new_game.tet_hard_drop, "L" : new_game.left_one, "R" : new_game.right_one, 
        "RL" : new_game.left_rotation, "RR" : new_game.right_rotation}

while new_game.playing == True:
    for turn in range(turns): 
        for event in pygame.event.get():  
            if event.type == pygame.QUIT: 
                new_game.playing = False
        #update tetramino que, if this is the first run itnitlize que with tets
        new_game.Draw_board() # draw current board states, if this is the first run this will be a new peice spawn
        Agent.current_game_state = new_game.bit_map
        move = Agent.get_action()
        movement_dict[move]()
        Agent.state_action.append([move,new_game.bit_map])
        new_game.update_tet_position()
        if new_game.dropped == True:
                break
        
    if new_game.dropped != True:
        new_game.drop_down_one()

    if new_game.dropped == True:
        new_game.place_tet()
        new_game.clear_line()   #check if there are any lines cleared, if there are this method also adds to the score and calcualtes a new level
        if new_game.check_game_end() != False:
            new_game.reset_tet()
            new_game.spawn_tet()

    new_game.redraw_board()
     #redraw board with new moves 
    pygame.display.flip()
    print(new_game.current_tet)
    time.sleep(0.5) 
    #get state, reward, done, action

print("GAME OVER")

import numpy as np
import pygame
from numpy import array, left_shift
from Tetris import Tetris
import time
from agent import *

Game = Tetris()
agent = Agent()
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
        new_game.temp_score = new_game.score

        agent.update_current_state(new_game.game_states())
        move = agent.get_action()

        movement_dict[move]() #make move 

        new_game.update_tet_position()

        if new_game.dropped == True:
            new_game.place_tet()
            new_game.clear_line()   #check if there are any lines cleared, if there are this method also adds to the score and calcualtes a new level
            if new_game.check_game_end() != False:
                new_game.reset_tet()
                new_game.spawn_tet()
                agent.memory_push([agent.current_state, move, new_game.game_states(), new_game.reward(), new_game.playing])
                break
        agent.memory_push([agent.current_state, move, new_game.game_states(), new_game.reward(), new_game.playing])
        
    if new_game.dropped != True:
        new_game.drop_down_one()

    print(new_game.current_tet, new_game.rotation)
    new_game.redraw_board()
     #redraw board with new moves 
    pygame.display.flip()
    #print(new_game.current_tet)
    time.sleep(0.3) 
    #get state, reward, done, action

print("GAME OVER")

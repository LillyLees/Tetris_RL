games = int(input("Games to run: "))
Training = input("Training Y/N: ").upper()


import numpy as np
import pygame
from numpy import array, left_shift
from Tetris import *
import time
from agent import *



pygame.font.init()

for game in range(games):
    new_game.reset_Game()
    turns = 8
    

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
            if move != "N":
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
        time.sleep(0.15) 
        #get state, reward, done, action

    new_game.reset_Game()

    print("GAME OVER")
    if Training == "Y":
        agent.train()

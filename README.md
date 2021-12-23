# Tetris_RL

## creating Tetris
- [x] create bored
- [X] generate random Tet 
- [X] implment scoring and levels 
- [X] finish coords for all tets
- [X] movement methods
### Test by making a default choice depending on what Tet is currently avialable 
- [X] compleated

## Getting Game states from bored 
- [ ] get max height
- [ ] get mind height
- [ ] Get score 
- [ ] het bumpyness 
- [X] get game states to return
this might not be nessary, instead a bitmap of the board will be outputted as long as the score 

### Test by making a a formula that based on hurtisics and Tet a certain rotation and line is chosen
- [X] compleated

## RL model
- [X] create state action que
- [X] implement greedy epsilon stratagy
- [X] start on CNN
- [X] create training loop in game loop
- [X] allow user to deffine weather agent trains
- [X] allow user to deffine how many rounds the Agent plays 
- [X] Agents traning is saved even if main is rum multiple times 
- [ ] When train method is called each element in the replay memeory is iterated thorough 
- [ ] sample mini batches from reply memory 
- [ ] generate Q values for each action - state pair

impliment CNN to analyse numpy array of board 

game state function should return score and board not current tet
current tet should not be stored in the transition it should only be used as input to the NN 
running lots at same times 

avrage random agent gets a score of 

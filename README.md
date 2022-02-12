# Tetris_RL

Model free Agent that seeks to maxamize episode length (made with PyTorch). 

Enviroment made with PyGame, moddled off OpenAI Gym enviro

Agent has default NN weighting and default leanring rate.
Takes whole board and current tet as game state. 
Loss reaches near convergence, game play dosent mesurably imporove. 
reward = (0.76 *lc) + (-0.37 * hol) + (-0.18 * bump) + (-0.51 * ah)

Agent2 has xavier_uniform NN initialization and  0.05 learning rate.
Takes top four rows of placed tets and current tet as game state. 
before learning rate and weighting changed seems to reach platue, not clearing lines

reward = (0.76 *lc) + (-0.37 * hol) + (-0.18 * bump) + (-0.51 * ah) + if is terminal (-100)

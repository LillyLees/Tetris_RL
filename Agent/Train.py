from TetAgent import *
import tqdm
import wandb

wandb.init(project="Tetris-RL", entity="forestlees") #importing wandb project

wandb.config = { #configuring wandb graph
  "learning_rate": 0.001,
  "epochs": 100,
  "batch_size": 128
}

num_episodes = int(input("Number of epidodes: ")) #user deffines how many episodes will train
ep_leng = int(input("Episode length [in steps]: ")) #user deffines the length of each episode

policy_net = torch.load('Nets/policy_net.ckpt') #loading latest trained policy net
target_net = torch.load('Nets/target_net.ckpt') #loading lastest trained target net

for i_episode in range(num_episodes):

    print(f'EPISODE {i_episode}')
    env.reset() # Initialize the environment and state

    cur_tet, board = env.get_state() #get current states 
    state = [board, cur_tet]
    avg_r = [] #creating a list of all rewards in a episode
    score_ = 0 #total score for the game

    for t in tqdm.tqdm(range(ep_leng)):
        # Select and perform an action
        action = select_action(state)
        _, reward, playing, _ = env.step(action) 

        avg_r.append(reward) #add reward to list of rewards. 
        reward = torch.tensor([reward], device=device) #convert int reward to tensor
        env.Render_m()

        #check if state is terminal and update next state array
        if playing:
            cur_tet, board = env.get_state()
            next_state = [board, cur_tet]
        else:
            next_state = None

        # Store the transition in memory
        memory.push(state, action, next_state, reward)
        env.Render_m()

        state = next_state # Move to the next state
        score_ = env.score # get current score

        #check if state is terminal and update episode duration
        if not playing:
            episode_durations.append(t + 1)
            break
        
        env.Render_m()

    # Update the target network, copying all weights and biases in DQN
    loss = optimize_model()

    #update wandb graphs
    wandb.log({"score": score_})
    wandb.log({"reward": sum(avg_r) / ep_leng})
    if type(loss) == int:
        wandb.log({"loss": loss})
    else:
        wandb.log({"loss": 0})
    
    #update target net every 10th episode
    if i_episode % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())

    #save changed netowrks every 200 episodes 
    if i_episode % 200 == 0:
        print("Saving")
        torch.save(policy_net, 'Nets/policy_net.ckpt')
        torch.save(target_net, 'Nets/target_net.ckpt') 

#save changed networks once all epusodes are finsihed 
torch.save(policy_net, 'Nets/policy_net.ckpt')
torch.save(target_net, 'Nets/target_net.ckpt') 


print('Complete')
env.close() #close enviroment







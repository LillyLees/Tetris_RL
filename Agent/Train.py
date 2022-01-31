from TetAgent import *

num_episodes = int(input("Number of epidodes: \n"))
Will_train = input("Train Y/N: \n").upper()
Speed = (100 - int(input("speed 0-100: \n"))) / 2
ep_leng = int(input("Episode length [in steps]: \n"))

if Will_train == "Y":
    Will_train = True
else:
    Will_train = False


for i_episode in range(num_episodes):
    print(f'EPISODE {i_episode}')
    # Initialize the environment and state
    env.reset()
    cur_tet, board = env.get_state()
    state = [board, cur_tet]

    for t in tqdm.tqdm(range(ep_leng)):
        # Select and perform an action
        action = select_action(state)

        _, reward, playing, _ = env.step(action)
        reward = torch.tensor([reward], device=device)
        
        env.Render_m()
        time.sleep(Speed)
    
        if playing:
            cur_tet, board = env.get_state()
            next_state = [board, cur_tet]

        else:
            next_state = None

        # Store the transition in memory
        memory.push(state, action, next_state, reward)
        env.Render_m()
        # Move to the next state
        state = next_state

        if not playing:
            episode_durations.append(t + 1)
            #plot_durations()
            break
        
        env.Render_m()
    # Update the target network, copying all weights and biases in DQN
    if Will_train == True:
        optimize_model()
    if i_episode % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())
    
print('Complete')

torch.save(policy_net, 'nets/policy_net.ckpt')
torch.save(target_net, 'nets/target_net.ckpt')

env.close()

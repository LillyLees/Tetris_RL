from TetAgent import *

num_episodes = int(input("Number of epidodes: "))

Speed = (100 - int(input("speed 0-100: "))) / 100
ep_leng = int(input("Episode length [in steps]: "))

policy_net = torch.load('nets/policy_net.ckpt')
target_net = torch.load('nets/target_net.ckpt')

losses = []
rewards = []


for i_episode in range(num_episodes):
    print(f'EPISODE {i_episode}')
    # Initialize the environment and state
    env.reset()
    cur_tet, board = env.get_state()
    state = [board, cur_tet]
    avg_r = []
    for t in tqdm.tqdm(range(ep_leng)):
        # Select and perform an action
        action = select_action(state)

        _, reward, playing, _ = env.step(action)
        reward = torch.tensor([reward], device=device)
        avg_r.append(int(reward[0]))

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
    
    rewards.append(sum(avg_r) / ep_leng)
    loss = optimize_model()
    if type(loss) == int:
        losses.append(loss)
    else:
        losses.append(0)
        
    if i_episode % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())
    

print(losses)
print(rewards)

#torch.save(policy_net, 'nets/policy_net.ckpt')
#torch.save(target_net, 'nets/target_net.ckpt')
print('Complete')


env.close()
pygame.quit()

plt.ion()
plt.scatter(rewards, losses)
plt.xlabel("Reward")
plt.ylabel("Loss")
plt.show()




import numpy as np
import game
import random
from copy import deepcopy

SIZE = 3
rewards, states, ls = game.generate_dataset(SIZE)
Q = np.zeros(rewards.shape)
# Set learning parameters
lr = 0.2
y = 0.9
num_episodes = 2000

rList = []
current_obs = 0
print(ls)
for i in range(num_episodes):
    s = current_obs
    current_obs += 1
    rAll = 0
    d = False
    j = 0
    while j < 99:
        j+=1
        a = np.argmax(Q[s,:] + np.random.randn(1, rewards.shape[1])*(1./(i+1)))
        print(a)
        new_state = states[s].reshape(SIZE**2)
        new_state[a] = 1
        indices = [item for sublist in np.argwhere(new_state == 0) for item in sublist]
        if not indices:
            break
        new_state[random.choice(indices)] = -1
        d, r = game.is_terminal_state(new_state.reshape((SIZE, SIZE)))
        if not d:
            s1 = ls.index(list(new_state))
            r = rewards[s, a]
        if d:
            Q[s, a] = Q[s, a] + lr * (r + y * np.max(r) - Q[s, a])
        else:
            Q[s, a] = Q[s, a] + lr * (r + y * np.max(Q[s1, :]) - Q[s, a])
        rAll += r
        s = s1
        if d == True:
            break
    rList.append(rAll)

print("Score over time: " + str(sum(rList)/num_episodes))
print("Final Q-Table Values")
print(Q)


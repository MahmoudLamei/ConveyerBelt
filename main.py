import sys
import numpy as np
import math
import random
import time
import gymnasium  as gym
import gym_game


def simulate():
    global epsilon, epsilon_decay
    # Looping on the number of episodes
    for episode in range(MAX_EPISODES):

        # Init environment
        state, info = env.reset()
        total_reward = 0

        # AI tries up to MAX_TRY times
        for t in range(MAX_TRY):
            # Draw game starting after episode 750
            if(episode > 750):
                env.render()
                # Delay to see the animation clearly
                time.sleep(0.1)

            # Encode the state as an array of two integers corresponding to two boxes
            stateSave = encode(state)

            # Pick a random action for box1 and box2 epsilon % of the time
            if random.uniform(0, 1) < epsilon:
                action1 = env.action_space.sample()
                action2 = env.action_space.sample()
            else:
                # Exploit the best q value and pick the best possible action for now
                action1 = np.argmax(q_table[stateSave[0]])
                action2 = np.argmax(q_table[stateSave[1]])

            # Manual rerouting for collision
            if(destination(state, [action1, action2]) == 0):
                action = encodeAction([action1, action2])
            elif(destination(state, [action1, action2]) == 1):
                action = encodeAction([action1, 6])
            else:
                if(action1 == 0):
                    action1 = 1
                elif(action1 == 1):
                    action1 = 0
                elif(action1 == 2):
                    action1 = 1
                elif(action1 == 3):
                    action1 == 4
                elif(action1 == 4):
                    action1 == 5
                elif(action1 == 5):
                    action1 == 4
                action = encodeAction([action1, 6])

            # Do action and get reward
            next_state, reward, terminated, truncated, info = env.step(action)
            # Adding the two rewards of the two boxes
            total_reward += reward[0] + reward[1]

            # Manual collision detection
            if(next_state[0][0] == next_state[1][0] and next_state[0][1] == next_state[1][1]):
                print(action1)

            # Get correspond q value from state, action pair for box1
            q_value = q_table[stateSave[0]][action1]
            # Get the best q value
            best_q = np.max(q_table[encode(next_state)[0]])

            # Adding new value to the q table using this equation
            # Q(state, action) <- (1 - a)Q(state, action) + a(reward + rmaxQ(next state, all actions))
            q_table[stateSave[0]][action1] = (
                1 - learning_rate) * q_value + learning_rate * (reward[0] + gamma * best_q)

            # Get correspond q value from state, action pair for box2
            q_value = q_table[stateSave[1]][action2]
            # Get best q value
            best_q = np.max(q_table[encode(next_state)[1]])

            # Adding new value to the q table using this equation
            # Q(state, action) <- (1 - a)Q(state, action) + a(reward + rmaxQ(next state, all actions))
            q_table[stateSave[1]][action2] = (
                1 - learning_rate) * q_value + learning_rate * (reward[1] + gamma * best_q)

            # Set up for the next iteration
            state = next_state

            # Draw game starting after episode 750
            if(episode > 750):
                env.render()
                # Delay to see the animation clearly
                time.sleep(0.1)

            # When episode is done, print reward
            if terminated or truncated or t >= MAX_TRY - 1:
                print("Episode %d finished after %i time steps with total reward = %f and epsilon = %g." % (
                    episode, t, total_reward, epsilon))
                env.reset()
                break

        # Exploring rate decay
        if epsilon >= 0.005:
            epsilon *= epsilon_decay

# Encoding the states to two integers


def encode(p):
    x = p[0][0]
    y = p[0][1]
    c1 = p[0][2]
    i1 = x // 2
    if(y % 2 == 0):
        i1 += (y//2) * 6 + (y//2) * 5
    else:
        i1 += (y//2) * 6 + (y//2 + 1) * 5

    x = p[1][0]
    y = p[1][1]
    c2 = p[1][2]
    i2 = x // 2
    if(y % 2 == 0):
        i2 += (y//2) * 6 + (y//2) * 5
    else:
        i2 += (y//2) * 6 + (y//2 + 1) * 5

    return ([i1 + (c1*38), i2 + (c2*38)])

# Encoding the two actions of the boxes to a number from 0 to 48


def encodeAction(a):
    a1 = a[0]
    a2 = a[1]
    i = 0
    while(a1 >= 1):
        i += 7
        a1 -= 1
    while(a2 >= 1):
        i += 1
        a2 -= 1
    return i

# Checking if the two boxes have the same destination (for collision)


def destination(pos, l):
    x1 = pos[0][0]
    y1 = pos[0][1]
    x2 = pos[1][0]
    y2 = pos[1][1]

    x1old = pos[0][0]
    y1old = pos[0][1]
    x2old = pos[1][0]
    y2old = pos[1][1]
    if l[0] == 0:
        x1 += 1
        y1 += 1
    if l[0] == 1:
        x1 += 2
    if l[0] == 2:
        x1 += 1
        y1 -= 1
    if l[0] == 3:
        x1 -= 1
        y1 -= 1
    if l[0] == 4:
        x1 -= 2
    if l[0] == 5:
        x1 -= 1
        y1 += 1

    if l[1] == 0:
        x2 += 1
        y2 += 1
    if l[1] == 1:
        x2 += 2
    if l[1] == 2:
        x2 += 1
        y2 -= 1
    if l[1] == 3:
        x2 -= 1
        y2 -= 1
    if l[1] == 4:
        x2 -= 2
    if l[1] == 5:
        x2 -= 1
        y2 += 1
    if(x1 == x2 and y1 == y2):
        return(1)
    if((x1 == x2old and y1 == y2old) and (x2 == x1old and y2 == y1old)):
        return(2)
    else:
        return(0)


# Main method
if __name__ == "__main__":
    env = gym.make("Pygame-v0", apply_api_compatibility=True)
    MAX_EPISODES = 9999
    MAX_TRY = 1000
    epsilon = 1
    epsilon_decay = 0.996
    learning_rate = 0.1
    gamma = 0.6
    q_table = np.zeros((114, 7))
    simulate()

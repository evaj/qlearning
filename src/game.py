from copy import deepcopy
from math import sqrt
import numpy as np


def generate_dataset(num_of_rows=3):
    actor = 1
    initial_state = np.zeros((num_of_rows, num_of_rows))
    all_states = []
    q_array = np.zeros((1, num_of_rows**2))
    new_row = np.zeros((1, num_of_rows**2))
    list_istate = initial_state.reshape(num_of_rows ** 2)
    all_list_states = []
    samples = get_next_round_samples(list_istate, -1)
    starting_samples = get_next_round_samples(list_istate, 1)
    curr_states = [initial_state]
    curr_states = samples + curr_states
    end = False
    while not end:
        new_states = []
        end = True
        list_states = []
        for state in curr_states:
            list_state = state.reshape(num_of_rows**2)
            ll = list(list_state)
            if ll not in all_list_states:
                list_states.append(list_state)
                all_list_states.append(ll)
                indices = [item for sublist in np.argwhere(list_state == 0) for item in sublist]
                if indices:
                    end = False
                q_array[-1][not indices] = -1
                for ind in indices:
                    new_state = deepcopy(list_state)
                    new_state[ind] = 1
                    new_states.append(new_state)
                    res, rew = is_terminal_state(new_state.reshape((num_of_rows, num_of_rows)))
                    q_array[-1][ind] = rew
                q_array = np.concatenate((q_array, new_row))
        all_states = all_states + deepcopy(list_states)
        curr_states = []
        for ns in new_states:
            curr_states = curr_states + get_next_round_samples(ns, -1)
    q_array = q_array[:-1]
    return q_array, all_states, all_list_states


def get_next_round_samples(state, actor):
    new_states = []
    # print(state)
    for index, elem in enumerate(state):
        if elem == 0:
            new_state = deepcopy(state)
            new_state[index] = actor
            # new_states = np.concatenate((new_states, new_state), axis=0)
            new_states.append(new_state.reshape((int(sqrt(state.shape[0])), int(sqrt(state.shape[0])))))
    # return new_states.reshape(((int(new_states.shape[0]/state.shape[0])), state.shape[0]))[1:]
    return new_states


def is_terminal_state(state_board):
    size = state_board.shape[0]
    for i in range(size):
        row_sum = state_board.sum(axis=0).sum()
        if abs(row_sum) == size:
            return True, np.sign(row_sum)
        row_sum = state_board.sum(axis=1).sum()
        if abs(row_sum) == size:
            return True, np.sign(row_sum)
        row_sum = np.trace(state_board)
        if abs(row_sum) == size:
            return True, np.sign(row_sum)
        row_sum = sum(state_board[i][size-i-1] for i in range(size))
        if abs(row_sum) == size:
            return True, np.sign(row_sum)
    return (False, 0) if np.any(state_board == 0) else (True, 0)

from copy import deepcopy
from math import sqrt
import numpy as np


class Board:
    def __init__(self, values, actor):
        self.values = values
        self.actor = actor

    def __hash__(self):
        return hash((tuple(self.values), self.actor))

    def perform_action_c(self, field, actor):
        new_board = deepcopy(self)
        new_board.values[field] = actor
        return new_board

    def is_terminal_state(self):
        val_array = np.array(self.values)
        size = int(sqrt(val_array.shape[0]))
        state_board = val_array.reshape((size, size))
        size = state_board.shape[0]
        for i in range(size):
            row_sum = state_board.sum(axis=0).sum()
            if abs(row_sum) == size:
                return True, np.sign(row_sum * self.actor)
            row_sum = state_board.sum(axis=1).sum()
            if abs(row_sum) == size:
                return True, np.sign(row_sum * self.actor)
            row_sum = np.trace(state_board)
            if abs(row_sum) == size:
                return True, np.sign(row_sum * self.actor)
            row_sum = sum(state_board[i][size - i - 1] for i in range(size))
            if abs(row_sum) == size:
                return True, np.sign(row_sum * self.actor)
        return (False, 0) if np.any(state_board == 0) else (True, 0)

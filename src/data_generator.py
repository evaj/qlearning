from tictactoe import Board
import numpy as np
from itertools import chain, permutations, combinations

#
# def powerset(iterable, min_attr):
#     xs = list(iterable)
#     return chain.from_iterable(combinations(xs, n) for n in range(min_attr, len(xs)+1))

def get_data(board_size, actor):
    board_length = board_size**2
    board = Board([0]*board_length, actor)
    return get_states([board], [])


def get_states(boards, all_boards):
    all_boards = list(all_boards)
    # boards  = set(boards)
    all_boards += [elem for elem in set(boards) - set(all_boards)]
    for board in boards:
        new_boards = []
        for index, field in enumerate(board.values):
            if field == 0:
                new_board = board.perform_action_c(index, board.actor)
                is_terminal, reward = board.is_terminal_state()
                new_boards.append(new_board)
                if is_terminal:
                    return []
        new_states = []
        for b in new_boards:
            new_states = new_states + get_new_states(b)
        new_states = set(new_states) - set(all_boards)
        all_boards = list(all_boards) + list(get_states(new_states, set(all_boards)))
    return set(all_boards)


def get_new_states(board):
    new_states = []
    for index, field in enumerate(board.values):
        if field == 0:
            new_states.append(board.perform_action_c(index, board.actor*(-1)))
    return new_states


# def combinations(iterable, r):
#     pool = tuple(iterable)
#     n = len(pool)
#     all_comb = []
#     for indices in permutations(range(n), r):
#         if sorted(indices) == list(indices):
#             all_comb.append(tuple(pool[i] for i in indices))
#     return all_comb


boards = get_data(3, 1)
print(len(boards))

# for comb in combinations([-1, 0, 1], 9):
#     print(comb)
"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_empty = 0
    for row in board:
        count_empty += row.count(EMPTY)
    if count_empty % 2 == 0:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    valid_actions = set()
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == EMPTY:
                valid_actions.add((row, col))
    return valid_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row, col = action
    board_copy = copy.deepcopy(board)
    if action not in actions(board):
        raise Exception
    if board_copy[row][col] is None:
        board_copy[row][col] = player(board_copy)
        return board_copy
    else:
        raise ValueError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check who has just been, only they can be a winner
    if player(board) == X:
        last_player = O
    else:
        last_player = X

    # Check rows
    for row in board:
        if row.count(last_player) == 3:
            return last_player

    # Check collumns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] == last_player:
            return last_player

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == last_player or board[2][0] == board[1][1] == board[0][2] == last_player:
        return last_player
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    def board_full(board):
        count_empty = 0
        for row in board:
            count_empty += row.count(EMPTY)
        if count_empty == 0:
            return True
    if winner(board) is not None or board_full(board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    if player(board) == X:
        plays = []
        for action in actions(board):
            plays.append([min_value(result(board, action)), action])
        return sorted(plays, key=lambda x: x[0], reverse=True)[0][1]
        # Max Player

    else:
        # Min player (O)
        plays = []
        for action in actions(board):
            plays.append([max_value(result(board, action)), action])
        return sorted(plays, key=lambda x: x[0], reverse=False)[0][1]



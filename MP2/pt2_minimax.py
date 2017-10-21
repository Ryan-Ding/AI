import random
import heapq

from copy import deepcopy
from pt2_board import Board

def defensive_heuristic_1(board, is_black):
    return 2 * len(board.get_pieces_set(is_black)) + random.random()

def defensive_heuristic_2(board, is_black):
    return 0

def offensive_heuristic_1(board, is_black):
    return 2 * (30 - len(board.get_pieces_set(not is_black))) + random.random()

def offensive_heuristic_2(board, is_black):
    return 8 - len(board.get_pieces_set(not is_black)) + \
           board.get_distance_to_enemy_base(is_black) + random.random()

def minimax_search(board, orig_is_black, is_black, is_max, turns):
    if turns == 0:
        if is_max:
            return (offensive_heuristic_2(board, orig_is_black), (0, 0), 0)
        else:
            return (defensive_heuristic_1(board, orig_is_black), (0, 0), 0)

    values = []
    for piece in board.get_pieces_set(is_black):
        for direction in range(3):
            if not board.moveable(piece, direction, is_black):
                continue
            board_copy = deepcopy(board)
            board_copy.move_piece(piece, direction, is_black)
            value = abs(minimax_search(board_copy, orig_is_black, not is_black, not is_max, turns - 1)[0])
            if is_max:
                heapq.heappush(values, (-value, piece, direction))
            else:
                heapq.heappush(values, (value, piece, direction))

    return heapq.heappop(values)

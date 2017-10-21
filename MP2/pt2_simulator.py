from pt2_minimax import minimax_search
from pt2_board import Board

board = Board()
is_black = 1
is_max = 1

print(board.grids)

while (board.winner == 0):
    value, piece, direction = minimax_search(board, is_black, is_black, is_max, 3)
    board.move_piece(piece, direction, is_black)
    is_black = not is_black
    is_max = not is_max
    print(board.grids)

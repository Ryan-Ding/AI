# The state of the board is stroed as a two dimensional array
# The meaning of each value in the array is as following:
# 0 = no piece at that grid
# 1 = a black piece
# 2 = a white piece
EMPTY = 0
BLACK = 1
WHITE = 2

# The direction by which a piece is moves is stored as:
# 0 = downward-left (for black) or upward-left (for white)
# 1 = downward (for black) or upward (for white)
# 2 = downward-right (for black) or upward-right (for white)
LEFTWARD = 0
STRAIGHT = 1
RIGHTWARD = 2

# The size of the borad is 8 * 8
SIZE = 8

class Board:
    def __init__(self):
        self.grids = []
        for x in range(2):
            self.grids.append([BLACK] * SIZE)
        for x in range(2, SIZE - 2):
            self.grids.append([EMPTY] * SIZE)
        for x in range(SIZE - 2, SIZE):
            self.grids.append([WHITE] * SIZE)

        self.winner = EMPTY
        self.black_pieces = set()
        self.white_pieces = set()
        for x in range(2):
            for y in range(SIZE):
                self.black_pieces.add((x, y))
        for x in range(SIZE - 2, SIZE):
            for y in range(SIZE):
                self.white_pieces.add((x, y))

    def moveable(self, position, direction, is_black):
        if is_black:
            return self.black_moveable(position, direction)
        else:
            return self.white_moveable(position, direction)

    def move_piece(self, position, direction, is_black):
        if is_black:
            self.move_black_piece(position, direction)
        else:
            self.move_white_piece(position, direction)

    def black_moveable(self, position, direction):
        x, y = position
        if x >= SIZE - 1:
            return False
        if direction == LEFTWARD:
            if y == 0 or self.grids[x + 1][y - 1] == BLACK:
                return False
        elif direction == STRAIGHT:
            if self.grids[x + 1][y] != EMPTY:
                return False
        else:
            if y == SIZE - 1 or self.grids[x + 1][y + 1] == BLACK:
                return False
        return True

    def white_moveable(self, position, direction):
        x, y = position
        if x <= 0:
            return False
        if direction == LEFTWARD:
            if y == 0 or self.grids[x - 1][y - 1] == WHITE:
                return False
        elif direction == STRAIGHT:
            if self.grids[x - 1][y] != EMPTY:
                return False
        else:
            if y == SIZE - 1 or self.grids[x - 1][y + 1] == WHITE:
                return False
        return True

    def move_black_piece(self, position, direction):
        x, y = position
        if direction == LEFTWARD:
            if self.grids[x + 1][y - 1] == WHITE:
                self.white_pieces.remove((x + 1, y - 1))    # capture white piece
            self.grids[x + 1][y - 1] = BLACK
            self.black_pieces.add((x + 1, y - 1))

        elif direction == STRAIGHT:
            self.grids[x + 1][y] = BLACK
            self.black_pieces.add((x + 1, y))

        else:
            if self.grids[x + 1][y + 1] == WHITE:
                self.white_pieces.remove((x + 1, y + 1))    # capture white piece
            self.grids[x + 1][y + 1] = BLACK
            self.black_pieces.add((x + 1, y + 1))

        self.grids[x][y] = EMPTY
        self.black_pieces.remove((x, y))
        if x + 1 == SIZE - 1 or len(self.white_pieces) == 0:
            self.winner = BLACK

    def move_white_piece(self, position, direction):
        x, y = position
        if direction == LEFTWARD:
            if self.grids[x - 1][y - 1] == 1:
                self.black_pieces.remove((x - 1, y - 1))    # capture black piece
            self.grids[x - 1][y - 1] = WHITE
            self.white_pieces.add((x - 1, y - 1))

        elif direction == STRAIGHT:
            self.grids[x - 1][y] = WHITE
            self.white_pieces.add((x - 1, y))

        else:
            if self.grids[x - 1][y + 1] == BLACK:
                self.black_pieces.remove((x - 1, y + 1))    # capture black piece
            self.grids[x - 1][y + 1] = WHITE
            self.white_pieces.add((x - 1, y + 1))

        self.grids[x][y] = EMPTY
        self.white_pieces.remove((x, y))
        if x - 1 == 0 or len(self.black_pieces) == 0:
            self.winner = WHITE

    def get_pieces_set(self, is_black):
        if is_black:
            return self.black_pieces
        else:
            return self.white_pieces

    def get_distance_to_enemy_base(self, is_black):
        if is_black:
            frontier = 1
            for piece in self.black_pieces:
                if piece[0] > frontier:
                    frontier = piece[0]
            return SIZE - 1 - frontier
        else:
            frontier = SIZE - 2
            for piece in self.white_pieces:
                if piece[0] < frontier:
                    frontier = piece[0]
            return frontier

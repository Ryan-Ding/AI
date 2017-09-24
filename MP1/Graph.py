

class Graph(object):
    """A Graph represent a maze.

    Attributes:
        start_position: A tuple of (row_index, col_index)
        goals: A list of tuples for all the goals in the maze

    Example usage:
        graph = Graph(path_to_file)
        path_to_goal = bfs(graph, graph.start_position, graph.goals[0])
    """

    def __init__(self, file_name):
        self.matrix = []
        self.start_position = None
        self.goals = []
        self.__parse_file(file_name)

    def get_neighbors(self, coords):
        """
        :type node: Node
        """
        coords_lst = Graph.__get_surrounding_coords(coords)
        neighbors = []
        for coords in coords_lst:
            if self.is_in_maze(coords) and not self.is_wall(coords):
                neighbors.append(coords)
        return neighbors

    def is_in_maze(self, coords):
        """
        :param coords: tuple (row, col)
        :return: boolean for whether the coords is in maze. The coords can be space, wall, or goal.
        """
        try:
            self.get_coords(coords)
            return True
        except IndexError:
            return False

    # The following functions can only be called if is_in_maze(coords) returns True.
    def get_coords(self, coords):
        """
        :param coords: tuple (row, col)
        :return: the character at coords
        """
        return self.matrix[coords[0]][coords[1]]

    def is_space(self, coords):
        return self.get_coords(coords) == ' '

    def is_wall(self, coords):
        return self.get_coords(coords) == '%'

    def is_goal(self, coords):
        return self.get_coords(coords) == '.'

    # private functions
    def __parse_file(self, file_name):
        with open(file_name, 'r') as maze_file:
            self.matrix = maze_file.read().splitlines()

        for i in range(len(self.matrix)):
            line = self.matrix[i]
            if self.start_position == None:
                index = line.find("P")
                if index != -1:
                    self.start_position = (i, index)
            self.__find_all_goals_in_line(i, line)

    def __find_all_goals_in_line(self, line_idx, line):
        start_idx = 0
        while True:
            start_idx = line.find('.', start_idx)
            if start_idx == -1:
                return
            self.goals.append((line_idx, start_idx))
            start_idx += 1

    @staticmethod
    def __get_surrounding_coords(coords):
        row = coords[0]
        col = coords[1]
        return [(row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col)]


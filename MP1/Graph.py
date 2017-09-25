
SINGLE_DOT_MAZES = ["mediumMaze.txt", "bigMaze.txt", "openMaze.txt"]
MULTI_DOT_MAZES = ["tinySearch.txt", "smallSearch.txt", "mediumSearch.txt"]

class Graph(object):
    """A Graph represent a maze.

    Attributes:
        start_position: A tuple of (row_index, col_index)
        goals: A list of tuples for all the goals in the maze
        visited: A set of tuples for all visited location

    Example usage:
        graph = Graph(path_to_file)
        path_to_goal = bfs(graph, graph.start_position, graph.goals[0])
    """

    def __init__(self, file_name):
        self.matrix = []
        self.visited = set()
        self.start_position = None
        self.goals = []
        self.came_from = {}     # For each node, which node it can most efficiently be reached from.
        self.steps_taken = 0    # Will only be updated if mark_solution() is called
        self.__parse_file(file_name)
        self.__maze_solved = False   # whether the matrix has been modified to print solution

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

    def has_visited(self, coords):
        return coords in self.visited

    def mark_visited(self, coords):
        self.visited.add(coords)


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

    # The following functions are used to get/print solution after a maze is solved
    def print_solution(self):
        if not self.__maze_solved:
            self.mark_solution()
        print("\nSolution:")
        self.print_maze()

    def get_maze_str(self):
        maze_str = "%d nodes expanded | %d steps taken \n"%(len(self.visited), self.steps_taken)
        for row in self.matrix:
            maze_str += "".join(row)
            maze_str += '\n'
        return maze_str

    def mark_solution(self):
        self.__maze_solved = True
        for goal in self.goals:
            pos_in_path = self.came_from[goal]
            while pos_in_path!=self.start_position:
                self.steps_taken += 1
                self.__set_coords(pos_in_path, ".")
                pos_in_path = self.came_from[pos_in_path]
        self.__set_coords(self.start_position, "P")

    def print_maze(self):
        print(self.get_maze_str())

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
            self.matrix[i] = list(self.matrix[i])

    def __find_all_goals_in_line(self, line_idx, line):
        start_idx = 0
        while True:
            start_idx = line.find('.', start_idx)
            if start_idx == -1:
                return
            self.goals.append((line_idx, start_idx))
            start_idx += 1

    def __set_coords(self, coords, character):
        self.matrix[coords[0]][coords[1]] = character

    @staticmethod
    def __get_surrounding_coords(coords):
        row = coords[0]
        col = coords[1]
        return [(row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col)]


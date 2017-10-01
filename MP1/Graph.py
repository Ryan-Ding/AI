SINGLE_DOT_MAZES = ["mediumMaze.txt", "bigMaze.txt", "openMaze.txt"]
MULTI_DOT_MAZES = ["tinySearch.txt", "smallSearch.txt", "mediumSearch.txt", "bigDots.txt"]

"""
search function's responsibility:
 - count nodes expanded
 - set node.parent, node.goals_left,...., every time a node is added to frontier
 - return last node (the node whose coords is the position of the last goal reached)
Node's responsibility:
 - keep track of parent node
Graph's responsibility:
 - keep track of which positions we have visited since last goal is reached
 - mark path on maze for both multidots and singledot maze (given the path or goals_reached in order)
"""

class Node(object):
    def __init__(self, coords):
        self.coords = coords
        self.parent = None
        self.goals_left = set()
        self.goals_reached = []  # append in order
        self.path_cost = 0  # "Every time you add a node to the frontier, check whether it already exists in the
                            # frontier with a higher path cost, and if yes, replace that node with the new one"
        self.f_score = 0

    def __lt__(self, other):
        if self.f_score < other.f_score:
            return True
        elif self.f_score > other.f_score:
            return False
        else:    # adding tie breaker when f_scores equal
            return len(self.goals_left) < len(other.goals_left)


    def __str__(self):
        if self.parent is not None:
            return '%s -> %s[%f]' % (self.parent.coords, self.coords, self.f_score)
        else:
            return "None -> %s[%f]" %(str(self.coords), self.f_score)

    def __repr__(self):
        return self.__str__()

    def get_path(self):
        reversed_path = []
        node = self
        while node.parent is not None:
            reversed_path.append(node.coords)
            node = node.parent
        reversed_path.reverse()
        return reversed_path

    def __eq__(self, other):
        if other is None:
            return False
        return self.coords == other.coords and self.goals_left == other.goals_left

    def __hash__(self):
        return hash(str(self.coords) + str(sorted(self.goals_left)))


class Graph(object):
    """A Graph represent a maze.

    Attributes:
        start_position: A tuple of (row_index, col_index)
        goals: A list of tuples for all the goals in the maze
        goals_left: A set of tuples for all the goals that have not been reached
        visited: A set of tuples for all visited location (QUESTION: need to empty this visited set everytime a goal is reached?)


    Example usage:
        graph = Graph(path_to_file)
        last_node = bfs_multi_dots(graph)
        graph.print_solution(last_node.get_path())
    """

    def __init__(self, file_name):
        self.matrix = []
        self.visited = set()
        self.start_position = None
        self.goals = []
        self.goals_left = set()  # Will be the same as self.goals at the beginning; every time a goal is reached
        self.__goals_reached = []  # stores reached goals in the order it was reached
        self.__parse_file(file_name)
        self.__maze_solved = False  # whether the matrix has been modified to print solution

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

    def reach_goal(self, coords):
        if coords in self.goals_left:
            self.goals_left.remove(coords)
            self.__goals_reached.append(coords)
            print("reached a goal! %d goals left: %s" % (len(self.goals_left), self.goals_left))
        else:
            if self.is_goal(coords):
                print("goal %s has already been reached before")
            else:
                print("%s is not a goal!" % coords)

    # The following functions are used to get/print solution after a maze is solved
    def print_solution(self, path, goals_reached):
        self.__mark_solution(path, goals_reached)
        print("\nSolution: %d steps taken" % len(path))
        self.print_maze()

    def get_maze_str(self):
        maze_str = ""
        for row in self.matrix:
            maze_str += "".join(row)
            maze_str += '\n'
        return maze_str

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
        self.goals_left = set(self.goals)

    def __mark_solution(self, path, goals_reached):
        self.__maze_solved = True
        if len(self.goals) > 1:
            for i in range(len(goals_reached)):
                self.__set_coords(goals_reached[i], Graph.__get_marker_for_goal(i))
            return
        else:
            for coords in path:
                self.__set_coords(coords, ".")

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

    @staticmethod
    def __get_marker_for_goal(goal_rank):
        if goal_rank < 10:
            return str(goal_rank)
        elif goal_rank - 10 < 26:
            return chr(ord("a") + (goal_rank - 10))
        else:
            return chr(ord("A") + (goal_rank - 36))


def mahattan_distance(origin, destination):
    return abs(destination[0] - origin[0]) + abs(destination[1] - origin[1])

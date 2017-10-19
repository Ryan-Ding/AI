class CSP:
    def __init__(self, filename):
        self.variables = set()
        self.all_colors = set()
        self.graph = None
        self.parse_graph(filename)

    def is_source(self, position):
        x, y = position
        return self.graph[x][y] != '_'

    def get_color(self, position):
        x, y = position
        return self.graph[x][y]

    def get_neighbors(self, position):
        pos_lst = CSP.__get_surrounding_positions(position)
        neighbors = []
        for neighbor_position in pos_lst:
            if self.is_on_graph(neighbor_position):
                neighbors.append(neighbor_position)
        return neighbors

    def is_complete(self, assignments):
        return len(assignments) == len(self.variables)

    def print_solution(self, assignments):
        height = len(self.graph)
        width = len(self.graph[0])
        for x in range(height):
            for y in range(width):
                position = (x,y)
                if position in self.variables:
                    color = assignments[position]
                else:
                    color = self.get_color(position)
                print(color, end='')
            print()

    def is_on_graph(self, position):
        x, y = position
        height = len(self.graph)
        width = len(self.graph[0])
        return width > x >= 0 and 0 <= y < height

    def parse_graph(self, filename):
        with open(filename, 'r') as maze_file:
            self.graph = maze_file.read().splitlines()

        for i in range(len(self.graph)):
            line = self.graph[i]
            self.graph[i] = list(line)
            for j in range(len(line)):
                c = line[j]
                if c == "_":
                    self.variables.add((i, j))
                else:
                    self.all_colors.add(c)

    def __get_surrounding_positions(position):
        row = position[0]
        col = position[1]
        return [(row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col)]

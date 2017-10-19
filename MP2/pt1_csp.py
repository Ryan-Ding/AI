
class CSP:
    def __init__(self, filename):
        self.variables = set()
        self.all_colors = set()
        self.graph = None
        self.parse_graph(filename)

    def parse_graph(self, filename):
        pass

    def is_source(self, position):
        pass

    def select_unassigned_variable(self, assignments):
        pass

    def get_neighbors(self, position):
        pass

    def is_complete(self, assignments):
        return len(assignments) == len(self.variables)
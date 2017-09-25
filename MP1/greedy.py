import MP1.Graph

def mahattan_distance(origin, destination):
    return abs(destination[0] - origin[0]) + abs(destination[1] - origin[1])

def greedy(graph):
    """

    :type graph: Graph
    """
    def h(coord):
        return mahattan_distance(graph.goals[0])



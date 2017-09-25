from MP1.Graph import Graph
import heapq

def mahattan_distance(origin, destination):
    return abs(destination[0] - origin[0]) + abs(destination[1] - origin[1])

def greedy(graph):
    def h(position):
        return mahattan_distance(position, graph.goals[0])

    # add first node to frontier
    frontier = []
    heapq.heappush(frontier, (h(graph.start_position), graph.start_position))
    while len(frontier)>0:
        distance, coords = heapq.heappop(frontier)
        print("distance: %d, coords: %s"%(distance, coords))
        graph.mark_visited(coords)
        if graph.is_goal(coords):
            return
        for neighbor in graph.get_neighbors(coords):
            if graph.has_visited(neighbor):
                continue
            graph.came_from[neighbor] = coords
            heapq.heappush(frontier, (h(neighbor), neighbor))

graph = Graph("mediumMaze.txt")
greedy(graph)
graph.print_solution()
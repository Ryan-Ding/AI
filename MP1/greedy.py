from math import log

from MP1.Graph import *
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
        graph.mark_visited(coords)
        if graph.is_goal(coords):
            return
        for neighbor in graph.get_neighbors(coords):
            if graph.has_visited(neighbor):
                continue
            graph.came_from[neighbor] = coords
            heapq.heappush(frontier, (h(neighbor), neighbor))


for maze in SINGLE_DOT_MAZES:
    graph = Graph(maze)
    greedy(graph)
    graph.print_solution()
    # with open(maze[:-4] +"_solution_greedy.txt", "w") as f:
    #     f.write(graph.get_maze_str())



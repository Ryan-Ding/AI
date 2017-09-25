from math import log

from MP1.Graph import *
import heapq


def greedy(graph):
    node_counts = 1

    def h(position):
        return mahattan_distance(position, graph.goals[0])

    # add first node to frontier
    frontier = []
    heapq.heappush(frontier, (h(graph.start_position), Node(graph.start_position)))
    while len(frontier) > 0:
        distance, node = heapq.heappop(frontier)
        graph.mark_visited(node.coords)
        if node.coords in graph.goals_left:
            graph.reach_goal(node.coords)
            if len(graph.goals_left) == 0:
                print("%d nodes expanded"%node_counts)
                return node

        for neighbor in graph.get_neighbors(node.coords):
            if graph.has_visited(neighbor):
                continue
            neighbor_node = Node(neighbor)
            neighbor_node.parent = node
            heapq.heappush(frontier, (h(neighbor), neighbor_node))
            node_counts += 1


for maze in SINGLE_DOT_MAZES:
    graph = Graph(maze)
    last_node = greedy(graph)
    graph.print_solution(last_node.get_path())
    # with open(maze[:-4] +"_solution_greedy.txt", "w") as f:
    #     f.write(graph.get_maze_str())

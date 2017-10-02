from collections import deque

from Graph import Graph
from queue import *

MAZE_NAME = "bigMaze"

def print_path(current_node, count):
    path_set = set()  # The set of all nodes on the solution path
    pos_on_path = current_node  # Initially the goal position

    while pos_on_path in came_from:  # Go back from goal to start position to retrive the nodes on path
        path_set.add(pos_on_path)
        pos_on_path = came_from[pos_on_path]

    with open("%s_bfs_soln.txt"%MAZE_NAME, "w") as fout:
        fout.write("%d nodes expanded | %d steps taken\n" % (count, len(path_set)))
        for i in range(len(graph.matrix)):
            for j in range(len(graph.matrix[i])):
                pos = (i, j)
                if pos in path_set:
                    fout.write(".")
                elif pos == graph.start_position:
                    fout.write("P")
                elif graph.is_space(pos):
                    fout.write(" ")
                elif graph.is_wall(pos):
                    fout.write("%")
            fout.write("\n")


def find_path(graph):
    node_count = 0
    start_pos = graph.start_position
    graph.mark_visited(start_pos)  # mark starting node as visited
    processing_queue.append(start_pos)  # add starting point to queue
    while len(processing_queue)>0:  # iterative bfs
        current_node = processing_queue.popleft()
        node_count += 1
        if current_node in graph.goals:  # goal state found
            print_path(current_node, node_count)
            return
        else:
            current_neighbors = graph.get_neighbors(current_node)  # get neighbors
            for neighbor in current_neighbors:  # iterate through neighbors
                if not graph.has_visited(neighbor):  # check if this node has been marked
                    graph.mark_visited(neighbor)
                    processing_queue.append(neighbor)
                    came_from[neighbor] = current_node  # remember parent


graph = Graph("%s.txt"%MAZE_NAME)
came_from = {}
processing_queue = deque()
find_path(graph)

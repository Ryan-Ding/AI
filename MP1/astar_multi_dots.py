import heapq

from MP1.Graph import *


def push_to_frontier(node_to_push, frontier):
    for score, node in frontier:
        if node == node_to_push:
            if node.path_cost < node_to_push.path_cost:
                node.parent = node_to_push.parent
                node.goals_reached = node_to_push.goals_reached
                node.path_cost = node_to_push.path_cost
            return
    heapq.heappush(frontier, (heuristic_estimate(node_to_push), node_to_push))

def evaluate(node):
    return node.path_cost + heuristic_estimate(node)

def heuristic_estimate(node):
    min_distance = 0
    for goal in node.goals_left:
        min_distance = min(min_distance, mahattan_distance(node.coords, goal))
    return min_distance

def update_score(frontier):
    new_frontier = []
    for score, node in frontier:
        heapq.heappush(new_frontier, (heuristic_estimate(node), node))


def find_path(graph):
    explored_set = set()
    frontier = []
    root = Node(graph.start_position)
    root.goals_left = set(graph.goals)
    heapq.heappush(frontier, (heuristic_estimate(root), root))
    while len(frontier):
        score, current_node = heapq.heappop(frontier)
        explored_set.add(current_node)
        if current_node.coords in current_node.goals_left:
            current_node.goals_left.remove(current_node.coords)
            print("reached a goal. goals left: ", current_node.goals_left)
            current_node.goals_reached.append(current_node.coords)
            if len(current_node.goals_left) == 0:
                print("expanded %d nodes" % (len(explored_set) + len(frontier)))
                return current_node

        current_neighbors = graph.get_neighbors(current_node.coords)
        for neighbor in current_neighbors:
            neighbor_node = Node(neighbor)
            neighbor_node.goals_left = set(current_node.goals_left)
            if neighbor_node in explored_set:
                continue
            neighbor_node.parent = current_node
            neighbor_node.goals_reached = list(current_node.goals_reached)
            neighbor_node.path_cost = current_node.path_cost + 1
            push_to_frontier(neighbor_node, frontier)

    # Will break out of loop if no path found.
    print("No path found")

graph = Graph("tinySearch.txt")
last_node = find_path(graph)
graph.print_solution(last_node.get_path(), last_node.goals_reached)

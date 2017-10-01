import heapq

from Graph import *
from kruskal import *


def evaluate(node):
    """
    :return: f(n) = g(n) + h(n)
    """
    return node.path_cost + heuristic_estimate(node)


def heuristic_estimate(node):
    """
    When solving the whole maze, use the score calculated based on the MST;
    when solving the partial maze, use manhattan distance to the closest goal.
    :return: h(n)
    """
    if full_graph:
        return MST_score(node)
    else:
        return distance_to_closest_goal(node)


################# heuristic candidates [start] #################

def distance_to_closest_goal(node):
    """
    :param node: current position node
    :return: the mahattan distance from current node to the closest goal
    """
    min_distance = float("inf")
    for goal in node.goals_left:
        min_distance = min(min_distance, mahattan_distance(node.coords, goal))
    return min_distance


def MST_score(node):
    """
    Finds the minimum spanning tree that connects all the goals left and the current position, where the weight of each
    edge is the actual shortest distance between two positions.
    :param node: current position node
    :return: a score calculated by summing the weights of all edges in the MST
    """
    global graph
    global shortest_distance_to_goal
    nodes_in_tree = set(node.goals_left)
    nodes_in_tree.add(node.coords)
    distances_btw_nodes = []
    for goal in node.goals_left:
        if node.coords not in shortest_distance_to_goal[goal]:
            shortest_distance_to_goal[goal][node.coords] = shortest_distance(graph, node.coords, goal)
        heapq.heappush(distances_btw_nodes, (shortest_distance_to_goal[goal][node.coords], node.coords, goal))
    for distance, goal1, goal2 in distances_btw_goals:
        if goal1 in node.goals_left and goal2 in node.goals_left:
            heapq.heappush(distances_btw_nodes, (distance, goal1, goal2))
    weights = kruskal_weight_sum(nodes_in_tree, distances_btw_nodes)
    return weights


################# heuristic candidates [end] #################

def shortest_distance(graph, point1, point2):
    """
    Calculate the actual shortest distance from point1 to point2 in graph using A* search with the manhattan distance as
    the heurisitc.
    """
    global full_graph
    full_graph = False  # solve a subproblem in maze
    last_node = find_path(graph, point1, set([point2]))
    distance = last_node.path_cost
    full_graph = True  # reset full_graph when switching back to solving the whole problem
    return distance


def find_path(graph, start_position, goals):
    """
    Find the shortest path for reaching all the goals from the start position in the graph.
    :return: the last node expanded (last_node.path will be the optimal path)
    """
    explored_set = set()
    node_count = 0
    frontier = []

    # push root to frontier
    root = Node(start_position)
    root.goals_left = set(goals)
    root.f_score = evaluate(root)
    heapq.heappush(frontier, root)

    # repeatedly expand frontier
    while len(frontier):
        current_node = heapq.heappop(frontier)
        node_count += 1
        explored_set.add(current_node)
        if current_node.coords in current_node.goals_left:  # a goal is reached
            current_node.goals_left.remove(current_node.coords)
            current_node.goals_reached.append(current_node.coords)
            if len(current_node.goals_left) == 0:
                print("expanded %d nodes" % node_count)
                return current_node
        # add current node's neighbors to frontier
        current_neighbors = graph.get_neighbors(current_node.coords)
        for neighbor in current_neighbors:
            neighbor_node = Node(neighbor)
            neighbor_node.goals_left = set(current_node.goals_left)
            # comment out the following two lines to search without repeated state detection
            if neighbor_node in explored_set:
                continue
            neighbor_node.parent = current_node
            neighbor_node.goals_reached = list(current_node.goals_reached)
            neighbor_node.path_cost = current_node.path_cost + 1
            push_to_frontier(neighbor_node, frontier)
    print("No path found")


def push_to_frontier(node_to_push, frontier):
    """
    Check if a node already exists in frontier before add it to frontier
    :param frontier: a heap of nodes
    """
    for i in range(len(frontier)):
        node = frontier[i]
        if node == node_to_push:  # if the state already exists in frontier
            if node.path_cost > node_to_push.path_cost:  # if the state we want to push has a smaller path_cost
                frontier.pop(i)  # remove the duplicated state with larger path_cost from frontier
                break
            else:
                return
    node_to_push.f_score = evaluate(node_to_push)
    heapq.heappush(frontier, node_to_push)


graph = Graph(MULTI_DOT_MAZES[0])
full_graph = False  # a boolean for whether the search is for the whole maze of part of the maze (i.e. solving subproblem)

# store the distances between each pair of positions for MST use
shortest_distance_to_goal = {}
for goal in graph.goals:
    shortest_distance_to_goal[goal] = {}

distances_btw_goals = []
for i in range(len(graph.goals)):
    for j in range(i + 1, len(graph.goals)):
        goal1 = graph.goals[i]
        goal2 = graph.goals[j]
        distance = shortest_distance(graph, goal1, goal2)
        distances_btw_goals.append((distance, goal1, goal2))
        shortest_distance_to_goal[goal1][goal2] = distance
        shortest_distance_to_goal[goal2][goal1] = distance

full_graph = True  # now search shortest path for the whole problem
last_node = find_path(graph, graph.start_position, graph.goals)
if last_node is not None:
    graph.print_solution(last_node.get_path(), last_node.goals_reached)
else:
    graph.print_maze()

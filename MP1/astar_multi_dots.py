import heapq

from MP1.Graph import *

"""
f(n) = g(n) + h(n)
f(n) -> evaluation function
g(n) -> path cost
h(n) -> heuristic function
"""
def evaluate(node):
    return node.path_cost  + heuristic_estimate(node)


################# heuristic candidates #################
def distance_to_furthest_goal(node):    # tested not consistent
    max_distance = 0
    for goal in node.goals_left:
        max_distance = max(max_distance, mahattan_distance(node.coords, goal))
    return max_distance


def distance_to_closest_goal(node):     # can find optimal, may be consistent (TODO: think proof)
    min_distance = float("inf")
    for goal in node.goals_left:
        min_distance = min(min_distance, mahattan_distance(node.coords, goal))
    return min_distance

def distance_to_all_goals(node):        # can find optimal solution, but doesn't look consistent
    all_distance = 0
    for goal in node.goals_left:
        all_distance += mahattan_distance(node.coords, goal) ** 0.5
    return all_distance

def num_of_goals_left(node):
    return len(node.goals_left)

################# heuristic candidates #################


def heuristic_estimate(node):
    return num_of_goals_left(node)


def find_path(graph):
    explored_set = set()
    frontier = []
    root = Node(graph.start_position)
    root.goals_left = set(graph.goals)
    root.f_score = evaluate(root)
    heapq.heappush(frontier, root)
    while len(frontier):
        current_node = heapq.heappop(frontier)
        explored_set.add(current_node)
        if current_node.coords in current_node.goals_left:
            current_node.goals_left.remove(current_node.coords)
            print("reached a goal. %d nodes in frontier. goals left: "%len(frontier), current_node.goals_left)
            current_node.goals_reached.append(current_node.coords)
            if len(current_node.goals_left) == 0:
                print("expanded %d nodes" % (len(explored_set) + len(frontier)))
                return current_node

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
    for i in range(len(frontier)):
        node = frontier[i]
        if node == node_to_push:
            if node.path_cost > node_to_push.path_cost:
                frontier.pop(i)
                break
            else:
                return
    node_to_push.f_score = evaluate(node_to_push)
    heapq.heappush(frontier, node_to_push)

graph = Graph(MULTI_DOT_MAZES[1])
last_node = find_path(graph)
if last_node is not None:
    graph.print_solution(last_node.get_path(), last_node.goals_reached)
else:
    graph.print_maze()

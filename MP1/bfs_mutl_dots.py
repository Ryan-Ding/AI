from collections import deque

from MP1.Graph import Graph, SINGLE_DOT_MAZES, MULTI_DOT_MAZES, Node


def has_explored(node, explored_set):
    return node in explored_set

def push_to_frontier(node_to_push, frontier):
    for node in frontier:
        if node == node_to_push:
            if node.path_cost < node_to_push.path_cost:
                node.parent = node_to_push.parent
                node.goals_reached = node_to_push.goals_reached
                node.path_cost = node_to_push.path_cost
            return
    frontier.append(node_to_push)


def find_path(graph):
    explored_set = set()
    node_count = 1
    frontier = deque()
    root = Node(graph.start_position)
    root.goals_left = set(graph.goals)
    frontier.append(root)

    while len(frontier)>0:
        current_node = frontier.popleft()
        explored_set.add(current_node)
        if current_node.coords in current_node.goals_left:
            current_node.goals_left.remove(current_node.coords)
            # print("reached a goal. goals left: ", current_node.goals_left)
            current_node.goals_reached.append(current_node.coords)
            if len(current_node.goals_left) == 0:
                print("expanded %d nodes" % node_count)
                return current_node
        current_neighbors = graph.get_neighbors(current_node.coords)
        for neighbor in current_neighbors:
            neighbor_node = Node(neighbor)
            neighbor_node.goals_left = set(current_node.goals_left)
            if has_explored(neighbor_node, explored_set):
                continue
            neighbor_node.parent = current_node
            neighbor_node.goals_reached = list(current_node.goals_reached)
            neighbor_node.path_cost += 1
            push_to_frontier(neighbor_node, frontier)
            node_count += 1
    print("didn't reach all the goals: ", current_node, current_node.goals_left, current_node.goals_reached)
    return current_node


graph = Graph(MULTI_DOT_MAZES[1])
last_node = find_path(graph)
path = last_node.get_path()

graph.print_solution(path, last_node.goals_reached)
print("%d steps taken:" % len(path), path)

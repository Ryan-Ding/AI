from queue import Queue

from MP1.Graph import Graph, SINGLE_DOT_MAZES, MULTI_DOT_MAZES, Node

def has_explored(node, explored_set):
    if node in explored_set:
        return True
    return False


def find_path(graph):
    explored_set = set()
    node_count = 1
    processing_queue = Queue()
    root = Node(graph.start_position)
    root.goals_left = set(graph.goals)
    processing_queue.put(root)

    while not processing_queue.empty():
        current_node = processing_queue.get()
        current_node.visited.add(current_node.coords)
        explored_set.add(current_node)
        if current_node.coords in current_node.goals_left:
            current_node.goals_left.remove(current_node.coords)
            print("reached a goal. goals left: ", current_node.goals_left)
            current_node.goals_reached.append(current_node.coords)
            if len(current_node.goals_left)==0:
                print("expanded %d nodes"%node_count)
                return current_node
            current_node.visited = set()
        current_neighbors = graph.get_neighbors(current_node.coords)
        for neighbor in current_neighbors:
            neighbor_node = Node(neighbor)
            neighbor_node.goals_left = set(current_node.goals_left)
            if has_explored(neighbor_node, explored_set):
                continue
            neighbor_node.parent = current_node
            neighbor_node.goals_reached = list(current_node.goals_reached)
            neighbor_node.visited = set(current_node.visited)
            neighbor_node.path_cost += 1
            processing_queue.put(neighbor_node)
            node_count += 1
    print("didn't reach all the goals: ", current_node, current_node.goals_left, current_node.goals_reached)
    return current_node


graph = Graph(MULTI_DOT_MAZES[0])
last_node = find_path(graph)
path = last_node.get_path()

graph.print_solution(path, last_node.goals_reached)
print("%d steps taken:"%len(path), path)
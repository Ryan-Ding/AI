from queue import Queue

from MP1.Graph import Graph, SINGLE_DOT_MAZES, MULTI_DOT_MAZES, Node


def find_path(graph):
    node_count = 1
    processing_queue = Queue()
    start_pos = graph.start_position
    processing_queue.put(Node(start_pos))
    while not processing_queue.empty():
        current_node = processing_queue.get()
        graph.mark_visited(current_node.coords)
        if current_node.coords in graph.goals_left:
            graph.reach_goal(current_node.coords)
            if len(graph.goals_left)==0:
                print("expanded %d nodes"%node_count)
                return current_node
            processing_queue = Queue()
            graph.visited = set()
        current_neighbors = graph.get_neighbors(current_node.coords)
        for neighbor in current_neighbors:
            if graph.has_visited(neighbor):
                continue
            neighbor_node = Node(neighbor)
            neighbor_node.parent = current_node
            processing_queue.put(neighbor_node)
            node_count += 1
    print("didn't reach all the goals!")
    return current_node


graph = Graph(MULTI_DOT_MAZES[2])
print(graph.goals_left)
print(graph.goals)
last_node = find_path(graph)
print(graph.goals)
graph.print_solution()
path = last_node.get_solution()
print("%d steps taken:"%len(path), path)
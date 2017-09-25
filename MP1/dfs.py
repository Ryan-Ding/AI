from Graph import Graph

def print_path(current_node):
    path_set = set()# The set of all nodes on the solution path
    pos_on_path = current_node       # Initially the goal position

    while pos_on_path in came_from:       # Go back from goal to start position to retrive the nodes on path
        path_set.add(pos_on_path)
        pos_on_path = came_from[pos_on_path]

    with open("mediumMaze_dfs_soln.txt", "w") as fout:
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
	start_pos = graph.start_position
	graph.mark_visited(start_pos)
	stack.append(start_pos)
	while stack:
		current_node = stack.pop()
		if current_node in graph.goals:
			print_path(current_node)
			return
		else:
			current_neighbors = graph.get_neighbors(current_node)
			for neighbor in current_neighbors:
				if not graph.has_visited(neighbor):
					graph.mark_visited(neighbor)
					stack.append(neighbor)
					came_from[neighbor]=current_node
			graph.mark_visited(current_node)
	return






graph = Graph("mediumMaze.txt")
came_from = {}
stack = list()
find_path(graph)

from Graph import Graph

MAZE_NAME = "bigMaze"
def find_path():
    node_count = 0
    while (len(frontier)):
        global current_pos
        current_pos = pos_lowest_f_score()
        if (current_pos == graph.goals[0]):
            print_solution(node_count)
            return

        frontier.remove(current_pos)
        node_count += 1
        graph.mark_visited(current_pos)
        current_neighbors = graph.get_neighbors(current_pos)

        for neighbor in current_neighbors:
            if graph.has_visited(neighbor):
                continue       # Ignore the neighbor if it is already evaluated.
            tentative_g_score = g_score[current_pos] + 1
            if neighbor not in frontier:
                frontier.add(neighbor)      # Discovered a new node
            elif tentative_g_score >= g_score[neighbor]:
                continue       # This is not a better path.

            # This path is the best until now. Record it!
            came_from[neighbor] = current_pos;
            g_score[neighbor] = tentative_g_score;
            f_score[neighbor] = g_score[neighbor] + heuristic_estimate(neighbor, graph.goals)

    # Will break out of loop if no path found.
    print("No path found")

def pos_lowest_f_score():
    lowest_f = float("inf")
    pos_lowest_f = ()
    for pos in frontier:
        f_score_from_this_position = f_score[pos]
        if f_score_from_this_position < lowest_f:
            lowest_f = f_score_from_this_position
            pos_lowest_f = pos
    return pos_lowest_f

def heuristic_estimate(pos, goals):
    horizontal = abs(pos[0] - goals[0][0])
    vertical = abs(pos[1] - goals[0][1])
    return horizontal + vertical       # using manhattan distance

def print_solution(node_count):
    path_set = set()      # The set of all nodes on the solution path
    pos_on_path = current_pos      # Initially the goal position

    while pos_on_path in came_from:     # Go back from goal to start position to retrive the nodes on path
        path_set.add(pos_on_path)
        pos_on_path = came_from[pos_on_path]

    with open("%s_solution_astar.txt"%MAZE_NAME, "w") as fout:
        fout.write("%d nodes expanded | %d steps taken\n"%(node_count, len(path_set)))
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

graph = Graph("%s.txt"%MAZE_NAME)
current_pos = ()
came_from = {}

frontier = set()       # The set of currently discovered nodes that are not evaluated yet.

g_score = {}        # For each node, the cost of getting from the start node to that node.
f_score = {}        # Through each node, the total cost of getting from the start node to the goal.

for i in range(len(graph.matrix)):
    for j in range(len(graph.matrix[i])):
        g_score[(i, j)] = float("inf")
        f_score[(i, j)] = float("inf")

frontier.add(graph.start_position)
g_score[graph.start_position] = 0
f_score[graph.start_position] = heuristic_estimate(graph.start_position, graph.goals)

find_path()

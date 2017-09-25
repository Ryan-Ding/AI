from Graph import Graph

def find_path():
    while (len(open_set)):
        global current_pos
        current_pos = pos_lowest_f_score()
        if (current_pos == graph.goals[0]):
            print_path()
            return

        open_set.remove(current_pos)
        closed_set.add(current_pos)
        current_neighbors = graph.get_neighbors(current_pos)

        for neighbor in current_neighbors:
            if neighbor in closed_set:
                continue       # Ignore the neighbor if it is already evaluated.
            tentative_g_score = g_score[current_pos] + 1
            if neighbor not in open_set:
                open_set.add(neighbor)      # Discovered a new node
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
    for pos in open_set:
        f_score_from_this_position = f_score[pos]
        if f_score_from_this_position < lowest_f:
            lowest_f = f_score_from_this_position
            pos_lowest_f = pos

    return pos_lowest_f

def heuristic_estimate(pos, goals):
    horizontal = abs(pos[0] - goals[0][0])
    vertical = abs(pos[1] - goals[0][1])
    return horizontal + vertical

def print_path():
    path_set = set()
    pos_on_path = current_pos

    while pos_on_path in came_from:
        path_set.add(pos_on_path)
        pos_on_path = came_from[pos_on_path]

    with open("openMaze_solution_astar.txt", "w") as fout:
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

graph = Graph("openMaze.txt")
current_pos = ()

closed_set = set()
open_set = set()
came_from = {}

g_score = {}
f_score = {}

for i in range(len(graph.matrix)):
    for j in range(len(graph.matrix[i])):
        if graph.is_wall((i, j)):
            closed_set.add((i, j))
        g_score[(i, j)] = float("inf")
        f_score[(i, j)] = float("inf")

open_set.add(graph.start_position)
g_score[graph.start_position] = 0
f_score[graph.start_position] = heuristic_estimate(graph.start_position, graph.goals)

find_path()

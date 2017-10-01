from Graph import Graph

def print_path(current_node, count):
    path_set = set()# The set of all nodes on the solution path
    pos_on_path = current_node       # Initially the goal position

    while pos_on_path in came_from:       # Go back from goal to start position to retrive the nodes on path
        path_set.add(pos_on_path)
        pos_on_path = came_from[pos_on_path]

    with open("openMaze_dfs_soln.txt", "w") as fout:
        fout.write("%d nodes expanded | %d steps taken\n"%(len(graph.visited), len(path_set)))
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
    count=1
    start_pos = graph.start_position
    graph.mark_visited(start_pos) #mark starting node as visited
    stack.append(start_pos)    #add starting point to stack
    while stack:   #iterative dfs
       current_node = stack.pop()
       if current_node in graph.goals:   #goal state found
         print_path(current_node,count)
         return
       else:
         current_neighbors = graph.get_neighbors(current_node)    #get neighbors
         for neighbor in current_neighbors:   #iterate through neighbors
          if not graph.has_visited(neighbor): #check if this node has been marked
              graph.mark_visited(neighbor)
              stack.append(neighbor)
              count+=1
              came_from[neighbor]=current_node   #remember parent
         graph.mark_visited(current_node)
    return






graph = Graph("openMaze.txt") #start a graph class
came_from = {}  #initiate empty set
stack = list()
find_path(graph)    #find path

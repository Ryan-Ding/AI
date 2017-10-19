from collections import Counter, deque

from pt1_csp import CSP


def get_current_color(csp, assignments, position):
    if csp.is_source(position):
        return csp.get_color(position)
    elif position in assignments:
        return assignments[position]
    else:
        return None


def can_assign(csp, var, val, assignments):
    global attempted_count
    attempted_count += 1
    assignments[var] = val
    # print("checking can_assign({},{})".format(var, val))

    if not is_valid(csp, assignments, var):
        del assignments[var]
        return False

    # print("checking neighbors if assign({},{})".format(var, val))
    neighbors = csp.get_neighbors(var)
    for neighbor in neighbors:
        if not is_valid(csp, assignments, neighbor):
            del assignments[var]
            return False
    return True


def is_valid(csp, assignments, position):
    neighbors = csp.get_neighbors(position)
    color = get_current_color(csp, assignments, position)

    is_src = csp.is_source(position)

    counter = Counter()
    for neighbor in neighbors:
        neighbor_color = get_current_color(csp, assignments, neighbor)
        if neighbor_color:
            counter[neighbor_color] += 1
    num_colored = sum(counter.values())
    num_empty = len(neighbors) - num_colored
    # print("pos: {} | counter: {}".format(position, counter))
    if not color:  # an empty spot, cannot be source
        if is_src:
            print("WARNING!!! src empty!!!!!!")
            exit(1)
        if num_colored == 0:
            return True
        else:
            max_cnt_color, max_cnt = counter.most_common(1)[0]
            return max_cnt <= 2
    same_color_count = counter[color]
    if is_src:
        if num_empty == 0:
            return same_color_count == 1
        else:
            return same_color_count <= 1 and num_empty + same_color_count >= 1
    else:
        if num_empty == 0:
            return same_color_count == 2
        else:
            return same_color_count <= 2 and num_empty + same_color_count >= 2


def domain_values(var, assignments, csp):
    return csp.all_colors


def select_unassigned_variable(csp, unassigned, assignments):
    return unassigned.pop()


def assign(var, val, assignments, csp):
    assignments[var] = val
    # print("assign: {} = {}".format(var, val))


def backtrack(assignments, unassigned, csp):
    graph_str = csp.solution_str(assignments)
    print(graph_str)
    # print("backtracking..... assigned {} vars, unassigned: {}".format(len(assignments), unassigned))
    if csp.is_complete(assignments):
        return assignments
    var = select_unassigned_variable(csp, unassigned, assignments)
    # print("selected {}".format(var))
    for val in domain_values(var, assignments, csp):
        # print("checking {} ?= {}".format(var, val))
        if can_assign(csp, var, val, assignments):
            assign(var, val, assignments, csp)
            result = backtrack(assignments, unassigned, csp)
            if result:  # found solution
                return result
            else:
                # print("removing assignment for {}".format(var))
                del assignments[var]
    unassigned.append(var)
    return False


i = 9

game_name = 'pt1_{0}{0}'.format(i)
game_file_name = game_name + '.txt'
solution_file_name = game_name + '_solution.txt'

csp = CSP(game_file_name)
attempted_count = 0
unassigned = deque(sorted(csp.variables))
final_assignments = backtrack({}, unassigned, csp)
solution = csp.solution_str(final_assignments)
print(solution)
print("{} attempted assignment".format(attempted_count))

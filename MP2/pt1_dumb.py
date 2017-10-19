from collections import Counter

from pt1_csp import CSP

def get_current_color(csp, assignments, position):
    if csp.is_source(position):
        return csp.get_color(position)
    elif position in assignments:
        return assignments[position]
    else:
        return None

def can_assign(csp, var, val, assignments):
    assignments[var] = val
    print("checking can_assign({},{})".format(var, val))

    if not is_valid(csp, assignments, var):
        del assignments[var]
        return False

    neighbors = csp.get_neighbors(var)
    for neighbor in neighbors:
        if not is_valid(csp, assignments, neighbor):
            del assignments[var]
            return False
    print("can assign({},{})!".format(var, val))
    return True

def is_valid(csp, assignments, position):
    neighbors = csp.get_neighbors(position)
    color = get_current_color(csp, assignments, position)
    if not color:
        return True

    counter = Counter()
    for neighbor in neighbors:
        neighbor_color = get_current_color(csp, assignments, neighbor)
        if neighbor_color:
            counter[neighbor_color] += 1
    num_colored = sum(counter.values())
    num_empty = len(neighbors) - num_colored
    same_color_count = counter[color]
    if num_empty == 0:
        if csp.is_source(position):
            return same_color_count == 1
        else:
            return same_color_count == 2
    else:
        return same_color_count <= 2


def domain_values(var, assignments, csp):
    return csp.all_colors

def select_unassigned_variable(csp, assignments):
    remaining_vars = csp.variables - set(assignments)
    return remaining_vars.pop()

def assign(var, val, assignments, csp):
    assignments[var] = val
    print("assign: {} = {}".format(var, val))


def backtrack(assignments,  csp):
    # print("backtrack({})".format(assignments))
    if csp.is_complete(assignments):
        return assignments
    var = select_unassigned_variable(csp, assignments)
    # print("selected {}".format(var))
    for val in domain_values(var, assignments, csp):
        # print("checking {} ?= {}".format(var, val))
        if can_assign(csp, var, val, assignments):
            assign(var, val, assignments, csp)
            result = backtrack(assignments,  csp)
            if result != False:
                return result
            else:
                print("removing assignment for {}".format(var))
                del assignments[var]
    return False


csp = CSP('pt1_55input_sample.txt')
final_assignments = backtrack({}, csp)
csp.print_solution(final_assignments)
print(final_assignments)


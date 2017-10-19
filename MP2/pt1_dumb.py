from pt1_csp import CSP

def can_assign(csp, var, val, assignments):
    neighbors = csp.get_neighbors(var)
    same_color_count = 0
    for neighbor in neighbors:
        if neighbor in assignments and assignments[neighbor] == val:
            same_color_count += 1
    return same_color_count <= 2

def domain_values(var, assignments, csp):
    return csp.all_colors

def select_unassigned_variable(csp, assignments):
    remaining_vars = csp.variables - set(assignments)
    return remaining_vars.pop()

def assign(var, val, assignments, csp):
    assignments[var] = val

def backtrack(assignments, remaining_values, csp):
    if csp.is_complete(assignments):
        return assignments
    var = select_unassigned_variable(csp, assignments)
    for val in domain_values(var, assignments, csp):
        if can_assign(var, val, assignments, csp):
            assign(var, val, assignments, csp)
            result = backtrack(assignments, remaining_values, csp)
            if result:
                return result
            else:
                del assignments[var]
    return False


csp = CSP('pt1_insput55_sample.txt')

def can_assign(var, val, remaining_values):
    return val in remaining_values[var]


def assign(var, val, assignments, remaining_values, csp):
    assignments[var] = val
    neighbors = csp.get_neighbors(var)
    for neighbor in neighbors:
        remove_neighbors_remaining(neighbor, assignments, remaining_values, csp)

def remove_neighbors_remaining(var, assignments, remaining_values, csp):
    pass
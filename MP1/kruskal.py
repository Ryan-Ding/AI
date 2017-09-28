import heapq

parent = dict()
rank = dict()

def make_set(vertice):
    parent[vertice] = vertice
    rank[vertice] = 0


def find(vertice):
    if parent[vertice] != vertice:
        parent[vertice] = find(parent[vertice])
    return parent[vertice]


def union(vertice1, vertice2):
    root1 = find(vertice1)
    root2 = find(vertice2)
    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root1] = root2
        if rank[root1] == rank[root2]: rank[root2] += 1


def kruskal_weight_sum(nodes, edges):
    global parent
    global rank
    for vertice in nodes:
        make_set(vertice)
    weights = 0
    while len(edges) > 0:
        weight, vertice1, vertice2 = heapq.heappop(edges)
        if find(vertice1) != find(vertice2):
            union(vertice1, vertice2)
            weights += weight
    # reset the data structures for next calculation
    parent = dict()
    rank = dict()
    return weights

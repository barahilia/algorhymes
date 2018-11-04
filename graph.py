'''graph representation, i/o and basic tools

Graph is a dictionary of sets. Keys - are the nodes, value - set of adjucent
nodes. It isn't required for nodes in keys to include all the nodes from values.
'''

from collections import defaultdict


def read_edgelist(pathname):
    g = defaultdict(set)

    with open(pathname) as f:
        for line in f:
            v, w = line.split()
            g[v].add(w)

    return g


def edges(g):
    for v, adjucent in g.items():
        for w in adjucent:
            yield v, w


def to_undirected(g):
    for v, w in edges(g):
        g[w].add(v)


def traverse(g, start):
    queue = [start]
    visited = {start}

    while queue:
        v = queue.pop()
        yield v
        assert v in visited

        for w in g[v]:
            if w not in visited:
                queue.append(w)
                visited.add(w)


def connected_components(g):
    'warning: implemented for undirected graphs only'

    covered = set()

    for v in g:
        if v not in covered:
            component = set(traverse(g, v))
            yield component

            covered |= component


def get_subgraph(g, nodes):
    subgraph = defaultdict(set)

    for v, w in edges(g):
        if v in nodes and w in nodes:
            subgraph[v].add(w)

    return subgraph


def write_edgelist(g, pathname):
    with open(pathname, 'w') as f:
        for v, w in edges(g):
            f.write('%s %s\n' % (v, w))

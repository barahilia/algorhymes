from itertools import count
from Queue import PriorityQueue


def bfs_v1(neighbors, start, do):
    """Implementation from Wikipedia"""
    q = []
    q.append(start)
    while len(q) > 0:
        a = q.pop()
        do(a)
        a.checked = True
        for b in neighbors(a):
            if not b.checked:
                q.append(b)


def bfs_v2(start, neighbors):
    """With generators, as suggested by a colegue"""
    queue = [start]
    visited = {start}

    while queue:
        node = queue.pop(0)
        yield node
        for neighbor in neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)


def bfs_v3(start, neighbors, priority=None):
    """Support priorities and rebuilding path leading to every reached node"""
    if priority is None:
        counter = count()
        priority = lambda node: next(counter)

    visited = {start}
    queue = PriorityQueue()
    queue.put((priority(start), start, None))

    while not queue.empty():
        _, node, prev = queue.get()
        yield node, prev

        for neighbor in neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.put((priority(neighbor), neighbor, node))

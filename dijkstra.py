from heapq import heappush, heappop
from collections import deque
from unittest import TestCase


class Unreachable(Exception):
    def __init__(self, start, end):
        msg = "%s is unreachable from %s" % (end, start)
        Exception.__init__(self, msg)


def dijkstra(g, start, end):
    dist = {start: 0}
    prev = {}
    heap = [(0, start)]
    done = set()

    while heap:
        _, v = heappop(heap)

        if v in done:
            continue

        if v == end:
            path = deque([end])
            while v != start:
                v = prev[v]
                path.appendleft(v)
            return list(path), dist[end]

        for w, edge in g[v]:
            if edge < 0:
                raise ValueError("negative weight edge")
            dist_through_v = dist[v] + edge
            if w not in dist or dist_through_v < dist[w]:
                dist[w] = dist_through_v
                prev[w] = v
                heappush(heap, (dist[w], w))

        done.add(v)

    raise Unreachable(start, end)


class DijkstraTest(TestCase):
    def test_single_node(self):
        g = { 'a': [] }
        self.assertEqual(
            dijkstra(g, 'a', 'a'),
            (['a'], 0)
        )

    def test_two_nodes(self):
        g = { 'a': [('b', 1)], 'b': [] }
        self.assertEqual(
            dijkstra(g, 'a', 'b'),
            (['a', 'b'], 1)
        )

    def test_unreachable(self):
        g = { 'a': [], 'b': [] }
        self.assertRaises(Unreachable, dijkstra, g, 'a', 'b')

    def test_negative_weight(self):
        g = { 'a': [('b', -1)], 'b': [] }
        self.assertRaises(ValueError, dijkstra, g, 'a', 'b')

    def test_loop(self):
        g = { 'a': [('b', 1), ('c', 5)], 'b': [('c', 1)], 'c': [] }
        self.assertEqual(
            dijkstra(g, 'a', 'c'),
            (['a', 'b', 'c'], 2)
        )


def path_in_square():
    n = 10
    vertexes = [(a, b) for a in xrange(n) for b in xrange(n)]
    bounce = set([(5, 5), (5, 6), (5, 7), (5, 8)])

    g = {v: [] for v in vertexes}
    for a in xrange(n-1):
        for b in range(n-1):
            if (a, b) in bounce: continue
            g[a, b].append(((a, b+1), 1))
            g[a, b].append(((a+1, b), 1))
    
    path, _ = dijkstra(g, (0, 0), (9, 7))
    path = set(path)

    for a in xrange(n):
        for b in xrange(n):
            print 'x' if (a, b) in bounce else 'o' if (a, b) in path else '.',
        print


if __name__ == '__main__':
    path_in_square()


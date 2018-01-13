from unittest import TestCase, main


def ts_recursive(g):
    enter = set()
    res = []

    def dfs(g, v):
        if v in enter: return
        enter.add(v)
        for w in g[v]: dfs(g, w)
        res.append(v)
    
    for v in g: dfs(g, v)
    
    res.reverse()
    return res


def ts_loop(g):
    enter, done = set(), set()
    res, stack = [], []
    for v in g:
        stack.append(v)
        while stack:
            w = stack.pop()
            if w in enter:
                if w not in done:
                    res.append(w)
                    done.add(w)
                continue
            stack.append(w)
            enter.add(w)
            for x in g[w]: stack.append(x)
    res.reverse()
    return res


ts = ts_loop


class TestToposort(TestCase):
    def test_entirely_disconnected_graph(self):
        # a b c
        g = {'a': [], 'b': [], 'c': []}
        self.assertEqual(ts(g), ['b', 'c', 'a'])

    def test_line_graph(self):
        # a -> b -> c
        g = {'a': ['b'], 'b': ['c'], 'c': []}
        self.assertEqual(ts(g), ['a', 'b', 'c'])

    def test_two_heads(self):
        # a,d -> b -> c
        g = {'a': ['b'], 'd': ['b'], 'b': ['c'], 'c': []}
        self.assertEqual(ts(g), ['d', 'a', 'b', 'c'])

    def test_two_tails(self):
        # a -> b -> c,d
        g = {'a': ['b'], 'b': ['c', 'd'], 'c': [], 'd': []}
        self.assertEqual(ts(g), ['a', 'b', 'c', 'd'])

    def test_diamond(self):
        # a -> b,c -> d
        g = {'a': ['b', 'c'], 'b': ['d'], 'c': ['d'], 'd': []}
        self.assertEqual(ts(g), ['a', 'b', 'c', 'd'])

    def test_double_diamond(self):
        # a -> b -> d 
        #    > c <
        # e -> f -> g
        g = {
            'a': ['b', 'c'], 'b': ['d'], 'c': ['d', 'g'], 'd': [],
            'e': ['c', 'f'], 'f': ['g'], 'g': []
        }
        self.assertEqual(ts(g), ['e', 'f', 'a', 'b', 'c', 'd', 'g'])


if __name__ == '__main__':
    main()

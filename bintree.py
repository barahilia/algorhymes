from unittest import TestCase, main


class Node:
    def __init__(self, a, b, value):
        self.a = a
        self.b = b
        self.value = value

    def __eq__(self, other):
        return other is not None and self.value == other.value


def compare(first, second):
    if first is None and second is None:
        return True

    return (first == second and
            compare(first.a, second.a) and
            compare(first.b, second.b))


class Tree(TestCase):
    def test_node(self):
        self.assertEquals(Node(None, None, 1).a, None)
        self.assertEquals(Node(None, None, 2).value, 2)
        self.assertEquals(Node(None, Node(None, None, 1), 0).b.value, 1)

    def test_compare(self):
        self.assertTrue(compare(None, None))
        self.assertFalse(compare(None, Node(None, None, 1)))
        self.assertTrue(compare(Node(None, None, 1), Node(None, None, 1)))


if __name__ == '__main__':
    main()

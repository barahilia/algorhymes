"""
      7  8  9
      *--*--*
      |     |
*--*--*--*--*
0  1  2  3  4

a = a + n = a + 2 * n -> n = 2 * n
There exist x such that x = 2 * x. Even better, x <= a + n, items total!
"""
from unittest import TestCase, main


class Link:
    def __init__(self, tail):
        self.tail = tail


def has_loop(l):
    single, double = l, l
    
    while (double and double.tail) is not None:
        single = single.tail
        double = double.tail.tail

        if single == double:
            return True

    return False


class LoopTest(TestCase):
    def test_linked_list(self):
        self.assertIsNone(Link(None).tail)
        self.assertIsNotNone(Link(Link(None)).tail)

    def test_list_with_loop(self):
        l1, l2 = Link(None), Link(None)
        l1.tail, l2.tail = l2, l1
        self.assertIsNotNone(l1.tail.tail.tail.tail.tail)

        l3 = Link(l1)
        self.assertIsNotNone(l3.tail.tail.tail.tail.tail)

    def test_no_loop_detection(self):
        self.assertFalse(has_loop(None))
        self.assertFalse(has_loop(Link(None)))
        self.assertFalse(has_loop(Link(Link(None))))
        self.assertFalse(has_loop(Link(Link(Link(None)))))
        self.assertFalse(has_loop(Link(Link(Link(Link(None))))))
        self.assertFalse(has_loop(Link(Link(Link(Link(Link(None)))))))

    def test_loop_detection(self): 
        l1 = Link(None)
        l1.tail = l1
        self.assertTrue(has_loop(l1))

        l2 = Link(Link(None))
        l2.tail.tail = l2
        self.assertTrue(has_loop(l2))

        l3 = Link(Link(None))
        l3.tail.tail = l3.tail
        self.assertTrue(has_loop(l3))


if __name__ == '__main__':
    main()

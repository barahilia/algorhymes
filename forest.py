"""Build forest graph from edges

Assuming forest is represented as a list of edges as list of child-parent pairs:

>>> l = ["A1 B", "C1 D", "A2 B", "C2 D", "A3 B"]

build a forest (list of trees) as a dictionary:

>>> {
>>>     "B": { "A1": {}, "A2": {}, "A3": {} },
>>>     "D": { "C1": {}, "C2": {} }
>>> }
"""

from unittest import TestCase


def build_forest(lines):
    descendants = {}
    patriarchs = {}

    for l in lines:
        module, father = l.split()

        if father == "None":
            if module not in descendants:
                descendants[module] = {}
                patriarchs[module] = descendants[module]
            continue

        if father not in descendants:
            descendants[father] = {}
            patriarchs[father] = descendants[father]

        if module in descendants:
            descendants[father][module] = descendants[module]
            assert module in patriarchs
            del patriarchs[module]
        else:
            descendants[module] = {}
            descendants[father][module] = descendants[module]

    return patriarchs


class TestForest(TestCase):
    def test_empty_dict_for_no_strings(self):
        self.assertEquals(build_forest([]), {})

    def test_one_class_no_interface(self):
        self.assertEquals(
            build_forest(["A None"]),
            {"A": {}}
        )

    def test_one_class_one_interface(self):
        self.assertEquals(
            build_forest(["A B"]),
            {"B": {"A": {}}}
        )

    def test_two_classes(self):
        self.assertEquals(
            build_forest(["A1 B", "A2 B"]),
            {"B": {"A1": {}, "A2": {}}}
        )

    def test_two_superclasses(self):
        self.assertEquals(
            build_forest(["A1 B", "C1 D", "A2 B", "C2 D", "A3 B"]),
            {
                "B": {"A1": {}, "A2": {}, "A3": {}},
                "D": {"C1": {}, "C2": {}}
            }
        )

    def test_grandfather(self):
        self.assertEquals(
            build_forest(["A B", "B C"]),
            {"C": {"B": {"A": {}}}}
        )
        self.assertEquals(
            build_forest(["B C", "A B"]),
            {"C": {"B": {"A": {}}}}
        )

    def test_long_list(self):
        self.assertEquals(
            build_forest(
                ["D B", "K I", "J H", "G C", "E B", "I H", "C A", "B A", "F C"]
            ),
            {
                "A": {
                    "B": {"D": {}, "E": {}},
                    "C": {"G": {}, "F": {}}
                },
                "H": {
                    "I": {"K": {}},
                    "J": {}
                }
            }
        )

from unittest import TestCase


def is_variable(x):
    return isinstance(x, str) and x.startswith('v')


def update_aliases(prev, (a, b)):
    "Update prev groups with a=b"
    cur = []
    if not is_variable(b):
        cur.append(frozenset([a]))
    for group in prev:
        if a in group and b in group:
            cur.append(group)
        elif a in group:
            if len(group) > 1:
                cur.append(group ^ {a})
        elif b in group:
            cur.append(group | {a})
        else:
            cur.append(group)
    return cur


def alias(*stmts):
    "Compute aliases of every variable at the end of every stmt"
    aliases = [[] for s in stmts]
    cur = []
    going_to_label = None
    labels = {}
    jumped_from_lines = set()

    line = 0
    while line < len(stmts):
        a, b = stmts[line]

        if a == 'goto':
            if line in jumped_from_lines:
                break
            jumped_from_lines.add(line)
            going_to_label = b
            if going_to_label in labels:
                line = labels[going_to_label]
                continue
        elif a == 'label':
            labels[b] = line
            if going_to_label == b:
                going_to_label = None
        else:
            if going_to_label is None:
                cur = update_aliases(cur, (a, b))
            else:
                line = line + 1
                continue

        aliases[line] = cur
        line = line + 1

    return aliases


class AliasTest(TestCase):
    def test_data_assignments(self):
        a = alias(
            ('v1', 1),
            ('v2', 2),
        )
        self.assertEqual(a, [
            [{'v1'}],
            [{'v2'}, {'v1'}],
        ])

    def test_one_alias(self):
        a = alias(
            ('v1', 1),
            ('v2', 'v1'),
        )
        self.assertEqual(a, [
            [{'v1'}],
            [{'v1', 'v2'}],
        ])

    def test_alias_and_reassignment(self):
        a = alias(
            ('v1', 1),
            ('v2', 'v1'),
            ('v1', 3),
        )
        self.assertEqual(a, [
            [{'v1'}],
            [{'v1', 'v2'}],
            [{'v1'}, {'v2'}],
        ])

    def test_realiasing(self):
        a = alias(
            ('v1', 1),
            ('v2', 'v1'),
            ('v1', 3),
            ('v2', 'v1'),
        )
        self.assertEqual(a, [
            [{'v1'}],
            [{'v1', 'v2'}],
            [{'v1'}, {'v2'}],
            [{'v1', 'v2'}],
        ])

    def test_forward_goto(self):
        a = alias(
            ('v1', 1),
            ('goto', 'a'),
            ('v2', 'v1'),
            ('label', 'a'),
            ('v1', 2),
        )
        self.assertEqual(a, [
            [{'v1'}],
            [{'v1'}],
            [], # XXX error here
            [{'v1'}],
            [{'v1'}],
        ])

    def test_backward_goto(self):
        a = alias(
            ('v1', 1),
            ('label', 'a'),
            ('v2', 'v1'),
            ('goto', 'a'),
            ('v1', 2),
        )
        self.assertEqual(a, [
            [{'v1'}],
            [{'v1', 'v2'}],
            [{'v1', 'v2'}],
            [],
            [],
        ])

    def test_interleaved_code(self):
        a = alias(
            ('goto', 'a'),
            ('v1', 1),
            ('label', 'a'),
            ('v2', 'v1'),
            ('goto', 'b'),
            ('v3', 3),
            ('label', 'b'),
            ('v1', 2),
            ('goto', 'a')
        )
        self.assertEqual(a, [
            [],
            [],
            [{'v1'}],
            [{'v1', 'v2'}],
            [],
            [],
            [],
            [{'v1'}],
            [],
        ])

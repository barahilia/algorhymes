#!/usr/bin/env python
from sys import argv
from networkx import read_edgelist
from networkx.drawing.nx_pydot import write_dot


if len(argv) != 2:
    print 'usage: ./edges_to_dot.py edges'
    exit(1)

edges_pathname = argv[1]
graph = read_edgelist(edges_pathname)

dot_pathname = edges_pathname + '.dot'
write_dot(graph, dot_pathname)

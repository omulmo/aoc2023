#! /usr/bin/env python3
from functools import reduce
from operator import mul
import sys
import re

def parse(inputs):
    directions = inputs[0]
    graph = {}
    for line in inputs[2:]:
        [node,left,right] = re.findall(r'([0-9A-Z]{3})', line)
        graph[node] = (left,right)
    return directions, graph

def num_steps(graph, pos, directions, offset=0):
    i = offset
    steps = 0
    while pos[-1] != 'Z':
        l,r = graph[pos]
        pos = l if directions[i] == 'L' else r
        i = (i+1) % len(directions)
        steps += 1
    return steps, pos, i

def one(inputs):
    directions, graph = parse(inputs)
    return num_steps(graph,'AAA',directions)

def find_cycle(graph, pos, directions):
    i = 0
    steps = 0
    state = {}
    while True:
        state[(pos,i)] = steps
        s, p, i = num_steps(graph,pos, directions, i)
        cycle = state.get((p,i),None)
        if not cycle:
            steps,pos = steps+s, p
        else:
            return steps

def factorize(values):
    factor=2
    while factor <= min(values):
        while all(v%factor == 0 for v in values):
            values = [v // factor for v in values]
        factor += 1
    return values
        
def two(inputs):
    directions, graph = parse(inputs)
    positions = [key for key in graph.keys() if key[-1]=='A']
    steps = [find_cycle(graph, pos, directions) for pos in positions]
    stride = reduce(mul,factorize(steps))
    n=stride
    while any(n%s != 0 for s in steps):
        n += stride
    return n


if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    inputs = [ line.strip() for line in (sys.stdin if len(sys.argv)<3 else open(sys.argv[2]))]
    print(function(inputs))

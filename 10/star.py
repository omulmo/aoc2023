#! /usr/bin/env python3
from collections import defaultdict
import sys

DIRECTIONS = {
    'N': {
        '|': 'N',
        '7': 'W',
        'F': 'E'
    },
    'S': {
        '|': 'S',
        'J': 'W',
        'L': 'E'
    },
    'E': {
        '-': 'E',
        'J': 'N',
        '7': 'S'
    },
    'W': {
        '-':'W',
        'F':'S',
        'L':'N'
    }
}

DXDY = {
    'N': (0,-1),
    'S': (0,1),
    'W': (-1,0),
    'E': (1,0)
}

def find_loop(world, i, j, direction):
    loop = []
    while True:
        loop.append((i,j))
        (dx,dy) = DXDY[direction]
        (i,j) = (i+dx, j+dy)
        if (i,j) == loop[0]:
            return loop
        pipe = world[i,j]
        direction = DIRECTIONS[direction].get(pipe, None)
        if not direction:
            return []

def one(world, _, __):
    ((i,j), _) = next(filter(lambda item: item[1]=='S', world.items()))
    loop_lengths = [ len(find_loop(world, i, j, direction)) for direction in 'NSEW' ]
    return max(loop_lengths) // 2


def find_range(f, items):
    a,b = sys.maxsize, 0
    for x in map(f, items):
        a = min(a,x)
        b = max(b,x)
    return (a,b+1)

def find_direction(p, q):
    (a,b),(c,d) = p,q
    dxdy = (c-a, d-b)
    return next(filter(lambda x:x[1] == dxdy, DXDY.items()))[0]

def area(polygon):
    s = 0
    n = len(polygon)
    for i in range(n):
        (xi,yi),(xi1,yi1) = polygon[i], polygon[(i+1)%n]
        s += xi*yi1 - xi1*yi
    return s // 2

def two(world, w, h):
    ((i,j), _) = next(filter(lambda item: item[1]=='S', world.items()))
    loop = sorted((find_loop(world, i, j, direction) for direction in 'NSEW'), key=lambda l:len(l), reverse=True)[0]
    edges = set(loop)

    #
    # TODO: an easier way to do this?
    # 1. Figure out if the loop runs clock-wise or counter-clockwise.
    # 2. Look on the inside of the loop and count all empties before next edge
    #
    LOOK = 'ESWN' if area(loop) > 0 else 'WNES'

    inside = set()
    n = len(loop)
    curr_dir = find_direction(loop[n-1],loop[0])
    for i in range(0, n-1):
        x,y = loop[i]
        prev_dir = curr_dir
        curr_dir = find_direction(loop[i], loop[i+1])
        for dir in set([prev_dir, curr_dir]):
            look = LOOK['NESW'.index(dir)]
            dx,dy = DXDY[look]
            x,y = (x+dx,y+dy)
            space=set()
            while 0<=x and x<w and 0<=y and y<h and not (x,y) in edges:
                space.add((x,y))         
                x,y = (x+dx,y+dy)
            if (x,y) in edges:
                inside.update(space)
    #print(f'inside: {inside}')
    return len(inside)

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    inputs = [ line.strip() for line in (sys.stdin if len(sys.argv)<3 else open(sys.argv[2]))]
    world = defaultdict(lambda: '.', [((i,j),token) for j,row in enumerate(inputs) for i,token in enumerate(row)])
    print(function(world, len(inputs[0]), len(inputs)))

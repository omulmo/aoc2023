#! /usr/bin/env python3
import sys

def mirrors(row, col):
    n=len(row)
    a,b =col-1, col
    while a>=0 and b<n:
        if row[a] != row[b]: return False
        a -= 1
        b += 1
    return True

def pivot(world):
    w = len(world[0])
    h = len(world)
    return [ [world[row][col] for row in range(h)] for col in range(w) ]

def find_mirror_split(world):
    candidates=list(range(1,len(world[0])))
    row = 0
    while len(candidates)>0 and row<len(world):
        candidates = [ col for col in candidates if mirrors(world[row], col) ]
        row += 1
    return candidates

def find_mirrors(world, ignore=(None,None)):
    ic,ir = ignore
    cols = [ c for c in find_mirror_split(world) if c != ic ]
    rows = [ r for r in find_mirror_split(pivot(world)) if r != ir ]
    assert(len(cols)<2 and len(rows)<2)
    return ((cols[0:1] or [None])[0],(rows[0:1] or [None])[0])

def points(world_value):
    c,r = world_value
    return 100*(r or 0) + (c or 0)

def rowcol_diff(a,b):
    (c1,r1),(c2,r2) = a,b
    return c1!=c2 or r1!=r2

def find_smudge(world):
    old_rowcol = find_mirrors(world)
    for (y,row) in enumerate(world):
        for (x,item) in enumerate(row):
            smudge = '.' if item == '#' else '#'
            world[y] = row[:x] + smudge + row[x+1:]
            rowcol = find_mirrors(world, old_rowcol)
            if rowcol != (None,None) and rowcol_diff(rowcol, old_rowcol):
                return points(rowcol)
        world[y] = row
    assert(False)

def parse(inputs):
    worlds=[]
    curr=[]
    for line in inputs:
        if line == '':
            worlds.append(curr)
            curr = []
        else:
            curr.append(line)
    worlds.append(curr)
    return worlds

def one(inputs):
    return sum(points(find_mirrors(world)) for world in parse(inputs))

def two(inputs):
    return sum(find_smudge(world) for world in parse(inputs))
    

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    inputs = [ line.strip() for line in (sys.stdin if len(sys.argv)<3 else open(sys.argv[2]))]
    print(function(inputs))

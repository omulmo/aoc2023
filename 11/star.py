#! /usr/bin/env python3
import sys    

def dist(p, q):
    (a,b),(c,d) = p,q
    return abs(a-c) + abs(b-d)

def parse(inputs, expansion_factor=2):
    stars = []
    w,h = len(inputs[0]), len(inputs)
    empty_columns = [ col for col in range(w) if all(inputs[j][col]=='.' for j in range(h)) ]
    dy = 0
    for y,row in enumerate(inputs):
        if all(c == '.' for c in row):
            dy += expansion_factor-1
            continue
        dx = 0
        for x,c in enumerate(row):
            if x in empty_columns:
                dx += expansion_factor-1
                continue
            if c == '#':
                stars.append((x+dx,y+dy))
    n = len(stars)
    return sum(dist(stars[i],stars[j]) for i in range(n) for j in range(i+1,n))

def one(inputs):
    return parse(inputs)


def two(inputs):
    return parse(inputs, expansion_factor=1_000_000)

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    inputs = [ line.strip() for line in (sys.stdin if len(sys.argv)<3 else open(sys.argv[2]))]
    print(function(inputs))

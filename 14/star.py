#! /usr/bin/env python3
import sys

DIRECTIONS={
    'N': (0,-1),
    'S': (0,1),
    'E': (1,0),
    'W': (-1,0)
}

def roll(direction, world,w,h):
    dx,dy = DIRECTIONS[direction]
    for y in range(h) if dy<0 else range(h-1,-1,-1):
        for x in range(w) if dx<=0 else range(w-1,-1,-1):
            if world[y][x] == 'O':
                i,j=x,y
                while 0<=i+dx and i+dx<w and 0<=j+dy and j+dy<h and world[j+dy][i+dx]=='.':
                    i,j = i+dx,j+dy
                if (i,j)!=(x,y):
                    world[j][i], world[y][x] = 'O', '.'

def spin(world,w,h):
    for d in 'NWSE':
        roll(d,world,w,h)
    return world

def calc_load(world, w, h):
    load = 0
    for y in range(h):
        load += (h-y) * sum(1 if world[y][x]=='O' else 0 for x in range(w))
    return load

def one(world,w,h):
    roll('N', world, w, h)
    return calc_load(world, w, h)

def calc_hash(world):
    return hash('\n'.join(''.join(row) for row in world))

def two(world,w,h):
    table={calc_hash(spin(world,w,h)) : 1}
    loads=[-1, calc_load(world,w,h)]
    spins=1
    goal = 1000000000

    while spins <= goal:
        _hash = calc_hash(spin(world,w,h))
        loads.append(calc_load(world,w,h))
        spins+=1

        if _hash in table:
            start = table[_hash]
            cycle = spins-start
            print(f'Found cycle: start={start} spins={spins} -> cycle={cycle}')
            offset = (goal-start) % cycle
            return loads[start+offset]
        else:
            table[_hash] = spins

    assert(False)

if __name__ == '__main__':
    task = '2' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    world = [ [ item for item in line.strip() ] for line in (open('14/sample.txt') if len(sys.argv)<3 else open(sys.argv[2]))]
    h = len(world)
    w = len(world[0])
    print(function(world,w,h))

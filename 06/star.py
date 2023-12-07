#! /usr/bin/env python3
from functools import reduce
from operator import mul
import sys
import re

def travelled(charge, time):
    '''distance travelled for a given charging time (optimum when charge = time/2)'''
    return charge * (time - charge)

def find_range(time, min_dist):
    '''binary search to find the range in which pressed time yields distance longer than min_dist'''
    max_t = min_t = time // 2
    dt = 1
    while dt < time//2:
        dt *= 2
    while dt>0:
        if travelled(max_t+dt, time) > min_dist:
            max_t += dt
        if travelled(min_t-dt, time) > min_dist:
            min_t -= dt
        dt = dt //2
    return min_t, max_t


def one(inputs):
    parse_line = lambda x : map(int, re.findall(r'(\d)', x))
    times = parse_line(inputs[0].split(":")[1])
    dists = parse_line(inputs[1].split(":")[1])
    races = zip(times,dists)
    combos=[]
    for time,dist in races:
        a,b = find_range(time, dist)
        combos.append(b-a+1)
    return reduce(mul, combos)


def two(inputs):
    parse_line = lambda x : int(''.join(re.findall(r'\d', x)))
    time = parse_line(inputs[0].split(":")[1])
    dist = parse_line(inputs[1].split(":")[1])
    a,b = find_range(time, dist)
    combos = (b-a+1)
    return combos

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    inputs = [ line.strip() for line in (sys.stdin if len(sys.argv)<3 else open(sys.argv[2]))]
    print(function(inputs))

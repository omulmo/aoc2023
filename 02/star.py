#! /usr/bin/env python3
from collections import defaultdict
from functools import reduce
from operator import mul
import sys
import re

def parse(line:str):
    [game,result] = line.split(':')
    id = int(re.findall(r'Game (\d+)', game)[0])
    rounds = result.split(';')
    return id, rounds


def possible(round):
    r = defaultdict(lambda: 0)
    for (n,color) in re.findall(r'(\d+) (\w+)', round):
        r[color] = int(n)
    return r['red']<=12 and r['green']<=13 and r['blue']<=14

def game_one(id,rounds):
    return id if all(possible(r) for r in rounds) else 0

def one(inputs):
    return sum(game_one(*parse(line)) for line in inputs)


def game_two(id, rounds):
    r = defaultdict(lambda: 0)
    for round in rounds:
        for (n,color) in re.findall(r'(\d+) (\w+)', round):
            r[color] = max(r[color],int(n))
    return reduce(mul, r.values())

def two(inputs):
    return sum(game_two(*parse(line)) for line in inputs)

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    inputs = [ line.strip() for line in (sys.stdin if len(sys.argv)<3 else open(sys.argv[2]))]
    print(function(inputs))

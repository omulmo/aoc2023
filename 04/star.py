#! /usr/bin/env python3
from collections import defaultdict
import sys
import re

def parse(line):
    [(card, winning, numbers)] = re.findall(r'Card[ ]*(\d+): (.*)\|(.*)$', line)
    winning = set(re.findall(r'(\d+)', winning))
    numbers = set(re.findall(r'(\d+)', numbers))
    result = winning.intersection(numbers)
    return int(card), len(result)

def one(inputs):
    f = lambda c,n: 0 if n==0 else 2**(n-1)
    return sum(f(*parse(line)) for line in inputs)

def two(inputs):
    results = dict([parse(line) for line in inputs])
    n_cards = 0
    q=list(results.keys())
    while len(q) > 0:
        card = q.pop()
        n_cards += 1
        n = results[card]
        if n>0:
            q.extend(range(card+1,card+n+1))
    return n_cards

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    inputs = [ line.strip() for line in (sys.stdin if len(sys.argv)<3 else open(sys.argv[2]))]
    print(function(inputs))

#! /usr/bin/env python3
from functools import reduce
from operator import sub
import sys

def list_of_diffs(sequence, index=-1):
    nums=[sequence[index]]
    curr=sequence
    while any(x != 0 for x in curr):
        curr = [curr[i+1]-curr[i] for i in range(0,len(curr)-1)]
        nums.append(curr[index])
    return nums[-1::-1]

def one(inputs):
    return sum(sum(list_of_diffs(seq)) for seq in inputs)

def two(inputs):
    return sum(reduce(lambda a,b: b-a, list_of_diffs(seq, 0)) for seq in inputs)

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    inputs = [ [int(x) for x in line.strip().split()] for line in (sys.stdin if len(sys.argv)<3 else open(sys.argv[2]))]
    print(function(inputs))

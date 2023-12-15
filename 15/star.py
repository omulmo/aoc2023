#! /usr/bin/env python3
from collections import OrderedDict
import sys

def calc_hash(s):
    h = 0
    for c in s:
        h = (h + ord(c))*17 % 256
    return h

def one(inputs):
    return sum(map(calc_hash, inputs[0].split(',')))


class Box(OrderedDict):
    def __init__(self, idx):
        self.idx = idx

    def pop(self,k):
        if k in self:
            super().pop(k)

    def power(self):
        return (self.idx+1) * sum((i+1) * v for i,(_,v) in enumerate(self.items()))
            

def two(inputs):
    boxes = [Box(i) for i in range(256)]
    for instr in inputs[0].split(','):
        if instr[-1] == '-':
            k=instr[:-1]
            boxes[calc_hash(k)].pop(k)
        else:
            k,v = instr.split('=')
            boxes[calc_hash(k)][k] = int(v)

    return sum(box.power() for box in boxes)


if __name__ == '__main__':
    task = '2' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    inputs = [ line.strip() for line in open('sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))

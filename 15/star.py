#! /usr/bin/env python3
import sys

def calc_hash(s):
    h = 0
    for c in s:
        h = (h + ord(c))*17 % 256
    return h

def one(inputs):
    return sum(map(calc_hash, inputs[0].split(',')))


class Box:
    def __init__(self, idx):
        self.index = idx
        self.tuples = []

    def add(self,k,v):
        i = self.find(k)
        if i is None:
            self.tuples.append((k,v))
        else:
            self.tuples[i] = (k,v)

    def find(self,key):
        t = self.tuples
        for i,(k,_) in enumerate(t):
            if k==key:
                return i
        return None
    
    def delete(self,k):
        i = self.find(k)
        if i is None:
            return
        self.tuples = self.tuples[:i] + self.tuples[i+1:]

    def power(self):
        return (self.index+1) * sum((i+1) * v for i,(_,v) in enumerate(self.tuples))
            

def two(inputs):
    boxes = [Box(i) for i in range(256)]
    for instr in inputs[0].split(','):
        if instr[-1] == '-':
            k=instr[:-1]
            boxes[calc_hash(k)].delete(k)
        else:
            k,v = instr.split('=')
            boxes[calc_hash(k)].add(k,int(v))

    return sum(box.power() for box in boxes)


if __name__ == '__main__':
    task = '2' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    inputs = [ line.strip() for line in open('sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))

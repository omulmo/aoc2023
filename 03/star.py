#! /usr/bin/env python3
from collections import defaultdict
from operator import mul
import sys

class Map:
    def __init__(self, inputs):
        self.map = defaultdict(lambda: '.', [((col,row),item) for row,line in enumerate(inputs) for col,item in enumerate(line)])
        self.w = len(inputs[0])
        self.h = len(inputs)

    def is_adjacent_to_symbol(self,col,row):
        for y in row-1,row,row+1:
            for x in col-1,col,col+1:
                if self.map[x,y] not in '0123456789.':
                    return True
        return False

    def find_numbers(self):
        for y in range(self.h):
            x=0
            while x<self.w:
                if self.map[x,y] in '0123456789':
                    stop = x+1
                    s = self.map[x,y]
                    while self.map[stop,y] in '0123456789':
                        s += self.map[stop,y]
                        stop += 1
                    yield (x,y,stop-x,int(s))
                    x = stop
                else:
                    x += 1

    def find_gears(self):
        nbors = {}
        for x,y,length,num in self.find_numbers():
            for j in y-1,y,y+1:
                for i in range(x-1,x+length+1):
                    nbors[i,j] = v = nbors.get((i,j),[])
                    v.append(num)
   
        for y in range(self.h):
            for x in range(self.w):
                if self.map[x,y] == '*':
                    v = nbors.get((x,y),[])
                    if len(v)==2:
                        yield mul(*v)

    def one(self):
        sum_parts=0
        for x,y,length,part_number in self.find_numbers():
            if any(self.is_adjacent_to_symbol(i,y) for i in range(x,x+length)):
                sum_parts += part_number

        return sum_parts;

    def __repr__(self):
        return '\n'.join(''.join(self.map[i,j] for i in range(self.w)) for j in range(self.w))

def one(inputs):
    m = Map(inputs)
    #print(m)
    return m.process()


def two(inputs):
    m = Map(inputs)
    return sum(m.find_gears())

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    inputs = [ line.strip() for line in open('test.txt' if len(sys.argv)<3 else sys.argv[2]) ]
    print(function(inputs))

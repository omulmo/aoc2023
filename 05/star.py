#! /usr/bin/env python3
import sys
import re
from sortedcontainers import SortedSet

def Ranges():
    return SortedSet(key= lambda a: a[0] )

class RangesLookup:
    def __init__(self):
        self.ranges = Ranges()
    def add(self, dest, src, length):
        self.ranges.add((src,src+length-1,dest))
    def get(self, key):
        i = 0
        (start,stop,dest) = self.ranges[i]
        while stop<key and i<len(self.ranges)-1:
            i += 1
            (start,stop,dest) = self.ranges[i]
        if key<start or stop<key:
            return key
        return dest + (key-start)
    def get_ranges(self, a,b):
        r=Ranges()
        i=0
        done=False
        (start,stop,dest) = self.ranges[i]
        while not done:
            (start,stop,dest) = self.ranges[i]
            if a<start:
                r.add((a,min(b,start-1)))
                a=min(b,start)
            if b>start and a<stop:
                r.add((dest + (a-start), dest + (min(stop,b)-start)))
                a=min(b,stop +1)
            i+=1
            done = b<=stop or i==len(self.ranges)
        if b>stop:
            r.add((a,b))
        return r

    def __repr__(self):
        return str(self.ranges)

def parse_map(inputs, row):
    row += 1  # header
    rl = RangesLookup()
    n = len(inputs)
    while row<n and len(inputs[row]) > 0:
        (a,b,c) = map(int, re.findall(r'(\d+)', inputs[row]))
        rl.add(a,b,c)
        row += 1
    row += 1  # delimiter
    return row, rl

def parse(inputs):
    seeds=list(map(int, re.findall(r'(\d+)', inputs[0])))
    row=2    
    lookups=[]
    while row < len(inputs):
        row, lookup = parse_map(inputs, row)
        lookups.append(lookup)
    return seeds, lookups

def one(inputs):
    seeds, lookups = parse(inputs)
    min_location = sys.maxsize
    for value in seeds:
        for lookup in lookups:
            value = lookup.get(value)
        min_location = min(min_location, value)
    return min_location

def two(inputs):
    seeds, lookups = parse(inputs)
    ranges = Ranges()
    for i in range(0,len(seeds),2):
        (value,length) = seeds[i:i+2]
        a,b=value,value+length-1
        ranges.add((a,b))

    for lookup in lookups:
        result = Ranges()
        for a,b in ranges:
            r =lookup.get_ranges(a,b)
            for value in r:
                result.add(value)
        ranges = result
    return ranges.pop(0)[0]

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    inputs = [ line.strip() for line in (sys.stdin if len(sys.argv)<3 else open(sys.argv[2]))]
    print(function(inputs))

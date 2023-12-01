#! /usr/bin/env python3
import sys

def one(inputs):
    pass

def two(inputs):
    pass

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    inputs = [ line.strip() for line in sys.stdin ]
    print(function(inputs))

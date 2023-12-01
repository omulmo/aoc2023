#! /usr/bin/env python3
from collections import defaultdict
import sys
import regex

numbers = 'zero|one|two|three|four|five|six|seven|eight|nine'

lookup = defaultdict(lambda x: str(x))
for i,v in enumerate(numbers.split('|')):
    lookup[v] = str(i)

def parse(line, pattern):
    matches = regex.findall(pattern, line, overlapped=True)
    value = lookup.get(matches[0],matches[0]) + lookup.get(matches[-1],matches[-1])
    return int(value)

def one(inputs):
    return sum([parse(line, '[0-9]') for line in inputs])

def two(inputs):
    return sum([parse(line, '[0-9]|'+numbers) for line in inputs])


if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    inputs = [ line.strip() for line in sys.stdin ]
    print(function(inputs))

#! /usr/bin/env python3
import sys
import regex

numbers = 'zero|one|two|three|four|five|six|seven|eight|nine'

lookup = numbers.split('|')
value = lambda x: lookup.index(x) if x in lookup else int(x)

def parse(line, pattern):
    m = regex.findall(pattern, line, overlapped=True)
    return 10*value(m[0]) + value(m[-1])

if __name__ == '__main__':
    pattern = '[0-9]' if sys.argv[1] == '1' else '[0-9]|'+numbers
    print(sum(parse(line, pattern) for line in open(sys.argv[2])))

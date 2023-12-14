#! /usr/bin/env python3
import sys
from collections import Counter, defaultdict

def place_token(s, a, b, token_length, indent=0):
    ind=' '*indent
    #print(f'{ind}  place_token: a,b={a,b} token={token_length} s={s[a:b+1]}')
    for i in range(a,b-token_length+1):
        #print(f'{ind}  place_token: i={i} str = {s[i:i+token_length]}')
        if '.' in s[i:i+token_length]:
            continue
        if '#' in s[a:i] or s[i+token_length] == '#':
            continue
        #print(f'{ind}  place_token: yielding {i}')
        yield i

def place_tokens(s, tokens, i=0, j=0, indent=0):
    if i==0:
        s += '.'
        #print(f'START: s={s} len={len(s)}   tokens={tokens}')
    ind=' '*indent
    #print(f'{ind}state: i={i} j={j}')
    if i >= len(s):
        return 1 if j == len(tokens) else 0
    if j == len(tokens):
        return 0 if '#' in s[i:] else 1

    remainder = sum(tokens[j+1:]) + len(tokens) - j - 1
    b = len(s) - remainder
    #print(f'{ind}remainder={remainder}')
    variants = [idx for idx in place_token(s, i, b, tokens[j], indent)]
    #print(f'{ind}variants={variants}')
    sub = [place_tokens(s, tokens, idx+tokens[j]+1, j+1, indent+4) for idx in variants]
    #print(f'{ind}substates={sub}')
    return sum(sub)


def combinations(line, multiply=1):
    s, order = line.split(' ')
    s = '?'.join([s]*multiply)
    order = list(map(int, order.split(',')))
    order *= multiply
    #print(f'[{line}]-> {s} {order}')
    return place_tokens(s,order)

def solve(inputs, multiply=1):
    return sum(combinations(line, multiply) for line in inputs)

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    multiply = 1 if task == '1' else 5

    inputs = [ line.strip() for line in open('12/debug.txt' if len(sys.argv)<3 else sys.argv[2]) ]
    print(solve(inputs, multiply))

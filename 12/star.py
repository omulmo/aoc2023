#! /usr/bin/env python3
import sys
from collections import Counter, defaultdict

def _combos(length, items):
    v=list(range(length+1))
    for i in range(items-1):
        u = [1]*(length+1)
        for i in range(2,length+1):
            u[i] = u[i-1] + v[i]
        v = u
    return v[-1]

class ComboCache(defaultdict):
    def __missing__(self, key):
        return _combos(*key)

combo_cache = ComboCache()

def all_combos(n, tokensizes, consume_all=False):
    combos={}
    start = len(tokensizes) if consume_all else 0
    for t in range(start,len(tokensizes)+1):
        if t==0:
            combos[0]=1
            continue
        tl = sum(tokensizes[:t]) + t - 1
        if tl > n: break
        length = n-tl+1
        combos[t] =combo_cache[(length,t)]
    return combos

def next_must_have(target):
    a= target.index('#')
    b= a+1
    while b<len(target) and target[b]=='#':
        b += 1
    return a,b-a


class MyCounter(Counter):
    def updateEx(self, counter, offset=0, factor=1):
        self.update(dict([ (i+offset,c*factor) for i,c in counter.items() ]))


def find_possible_slots(target, tokensizes, consume_all=False):
    token_length_before = lambda j: sum(tokensizes[:j]) + max(0, j)

    must_find = '#' in target
    if len(tokensizes)==0:
        return "error" if must_find else Counter([0])

    n = len(target)
    if must_find and tokensizes[0]>n: return "error"

    if not must_find:
        c = all_combos(n, tokensizes, consume_all)
        return c

    res = MyCounter()
    i,tl = next_must_have(target)

    for j,ts in enumerate(tokensizes):
        tlb = token_length_before(j)
        if tlb > i:
            break
        if ts<tl:
            continue

        for k in range(max(tlb,i+tl-ts),i+1):
            if k+ts > n:
                continue
            if (target[k+ts] == '#' if k+ts<n else False):
                continue
            if tlb==0:
                multiplier = 1
            else:
                combos = find_possible_slots(target[:k-1], tokensizes[:j], consume_all=True)
                multiplier = "error" if combos == "error" else combos.get(j, "error")

                if multiplier == "error":
                    continue

            c = find_possible_slots(target[k+ts+1:], tokensizes[j+1:], consume_all=consume_all)
            if c=="error": continue
            res.updateEx(c, j+1, multiplier)

    if consume_all:
        a = len(tokensizes)
        b = res.get(a, "error")
        result = "error" if b=="error" else {a:b}
    else:    
        result = "error" if len(res)==0 and must_find else res

    return result


def match(targets, tokens):
    if len(targets)==0:
        return 1 if len(tokens)==0 else "error"
    
    combos = find_possible_slots(targets[0], tokens, consume_all=(len(targets)==1))
    if combos == "error": return "error"

    s=0
    for (ntokens, count) in combos.items():
        if len(tokens) < ntokens: continue
        x = match(targets[1:], tokens[ntokens:])
        if x == "error": continue
        s += x*count

    return s

def combinations(line, multiply):
    s, order = line.split(' ')
    s = '?'.join([s]*multiply)
    targets = [ x for x in s.split('.') if len(x)>0 ]
    tokensizes = list(map(int, order.split(',')))
    tokensizes *= multiply
    return match(targets, tokensizes)

def solve(inputs, multiply=1):
    s = 0
    for (i,line) in enumerate(inputs):
        x = combinations(line, multiply)
        print(f'Line: {i:3d} -> {x}')
        s += x
    return s

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    multiply = 1 if task == '1' else 5

    inputs = [ line.strip() for line in open('12/sample.txt' if len(sys.argv)<3 else sys.argv[2]) ]
    print(solve(inputs, multiply))

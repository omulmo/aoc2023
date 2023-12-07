#! /usr/bin/env python3
from collections import defaultdict
import sys

HAND = 'AKQJT98765432'

class Score:
    HighCard = 1
    OnePair = 2
    TwoPairs = 3
    Threes = 4
    FullHouse = 5
    Four = 6
    Five = 7

    @staticmethod
    def no_jokers(cards):
        counter = defaultdict(int)
        for card in cards:
            counter[HAND.index(card)] += 1
        v = list(counter.values())
        if 5 in v:
            return Score.Five
        elif 4 in v:
            return Score.Four
        elif 3 in v:
            return Score.FullHouse if 2 in v else Score.Threes
        elif 2 in v:
            return Score.TwoPairs if v.count(2)==2 else Score.OnePair
        else:
            return Score.HighCard

    @staticmethod
    def with_jokers(cards):
        counter = defaultdict(int)
        for card in cards:
            counter[HAND.index(card)] += 1
        j = HAND.index('J')
        jokers = counter[j]
        counter[j] = 0
        v = list(counter.values())
        if 5 in v:
            return Score.Five
        elif 4 in v:
            return [Score.Four, Score.Five][jokers]
        elif 3 in v:
            return [Score.FullHouse if 2 in v else Score.Threes, Score.Four, Score.Five][jokers]
        elif 2 in v:
            return [ Score.TwoPairs if v.count(2)==2 else Score.OnePair,
                    Score.FullHouse if v.count(2)==2 else Score.Threes,
                    Score.Four,
                    Score.Five ][jokers]
        else:
            return [Score.HighCard, Score.OnePair, Score.Threes, Score.Four, Score.Five, Score.Five][jokers]


class Hand:
    def __init__(self, cards, bid, with_jokers=False):
        self.cards = cards
        self.bid = bid
        self.jokers = with_jokers
        self.score = Score.with_jokers(cards) if with_jokers else Score.no_jokers(cards)

    @staticmethod
    def parse(line, with_jokers=False):
        h,b = line.split(' ')
        return Hand(h, int(b), with_jokers)

    def __lt__(self, other):
        ORDER = 'AKQT98765432J' if self.jokers else 'AKQJT98765432'
        if self.score != other.score:
            return self.score < other.score
        for (s,o) in zip(self.cards, other.cards):
            if s==o: continue
            return ORDER.index(s) > ORDER.index(o)
        return NotImplemented

    def __repr__(self):
        return f'{self.cards} ({self.score})'


def one(inputs):
    hands = sorted([ Hand.parse(line) for line in inputs ])
    #print(hands)
    score = 0
    for i,hand in enumerate(hands):
        score += (i+1) * hand.bid
    return score


def two(inputs):
    hands = sorted([ Hand.parse(line, with_jokers=True) for line in inputs ])
    score = 0
    for i,hand in enumerate(hands):
        score += (i+1) * hand.bid
    return score

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    inputs = [ line.strip() for line in (sys.stdin if len(sys.argv)<3 else open(sys.argv[2]))]
    print(function(inputs))

#! /usr/bin/env python3

import unittest
from parameterized import parameterized
from old import place_token, place_tokens, combinations as old_combinations
from star import combinations, find_possible_slots

SAMPLE='''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
.?.????????.? 5,1'''.splitlines()

class Test1(unittest.TestCase):
    def testTokenCombos(self):
        self.assertEqual(list(place_token('.#.', 0, 2, 1)), [1])
        self.assertEqual(list(place_token('.#.', 1, 2, 1)), [1])
        self.assertEqual(list(place_token('#.', 0, 1, 1)), [0])
        self.assertEqual(list(place_token('##.', 0, 2, 2)), [0])
        self.assertEqual(list(place_token('##?', 0, 2, 2)), [0])
        self.assertEqual(list(place_token('###', 0, 2, 2)), [])
        self.assertEqual(list(place_token('#?#.', 0, 3, 3)), [0])
        self.assertEqual(list(place_token('?###?', 0, 5, 3)), [1])


class Test2(unittest.TestCase):
    @parameterized.expand([
        ('#', [1], {1:1}),
        ('?#?#', [1,1], {2:1}),
        ('???', [1], {0:1, 1:3}),
        ('##', [1], "error"),
        ('?##', [3,1], {1:1}),
        ('?##?', [2], {1:1}),
        ('??#???', [3,1], {1:3, 2:3}),
        ('?##', [3,1], {1:1}),
        ('???', [2], {0:1, 1:2}),
        ('?##??', [3,1], {1:2, 2:1}),
        ('????##????', [3,3,2], {1:1, 2:1, 3:2}),
    ])
    def testSlots(self, s, tokenlen, expected):
        r = find_possible_slots(s, tokenlen)
        self.assertCountEqual(r, expected)

    def testX(self):
        c = find_possible_slots('?##', [1,3])
        self.assertCountEqual(c, "error")


class Test3(unittest.TestCase):
    @parameterized.expand([
        (0,1),(1,4),(2,1),(3,1),(4,4),(5,10),(6,7)
    ])
    def test1(self, idx, expected):
        self.assertEqual(old_combinations(SAMPLE[idx], 1), expected)
        self.assertEqual(combinations(SAMPLE[idx], 1), expected)

    @parameterized.expand([
        (0,1),(1,16384),(2,1),(3,16),(4,2500),(5,506250)
    ])
    def test2(self, idx, expected):
        self.assertEqual(combinations(SAMPLE[idx], 5), expected)


class TestFinal(unittest.TestCase):
    @parameterized.expand([
        ('.#.#',[1,1],1),
        ('.?.#',[1,1],1),
        ('??.#',[1,1],2),
        ('#.#.###',[1,1,3],1),

        ('???.###', [1,1,3], 1),
        ('.??..??...?##.', [1,1,3], 4),
        ('?#?#?#?#?#?#?#?', [1,3,1,6], 1),
        ('????.#...#...', [4,1,1], 1),
        ('????.######..#####.', [1,6,5], 4),        
        ('?###????????', [3,2,1], 10)
    ])
    def test(self, s, tokens, expected):
        self.assertEqual(place_tokens(s, tokens), expected)


if __name__ == '__main__':
    unittest.main(failfast=True)

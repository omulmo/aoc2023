#! /usr/bin/env python3

import unittest
from star import parse

DATA = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''.splitlines()

class Test1(unittest.TestCase):
    def testA(self):
        self.assertEqual(parse(DATA), 374)

    def testB(self):
        self.assertEqual(parse(DATA, 10), 1030)

    def testC(self):
        self.assertEqual(parse(DATA, 100), 8410)

if __name__ == '__main__':
    unittest.main()

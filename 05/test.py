#! /usr/bin/env python3

import unittest
from star import RangesLookup

class Test1(unittest.TestCase):
    def testRangeLookup(self):
        rl = RangesLookup()
        rl.add(50,98,2)
        rl.add(52,50,48)
        self.assertEqual(rl.get(0), 0)
        self.assertEqual(rl.get(1), 1)
        self.assertEqual(rl.get(48), 48)
        self.assertEqual(rl.get(49), 49)
        self.assertEqual(rl.get(50), 52)
        self.assertEqual(rl.get(51), 53)
        self.assertEqual(rl.get(97), 99)
        self.assertEqual(rl.get(98), 50)
        self.assertEqual(rl.get(99), 51)
        self.assertEqual(rl.get(100), 100)
        print(rl.get_ranges(0,1))
        print(rl.get_ranges(0,49))
        print(rl.get_ranges(52,54))
        print(rl.get_ranges(0,50))
        print(rl.get_ranges(0,101))

class Test2(unittest.TestCase):
    def testTwo(self):
        pass

if __name__ == '__main__':
    unittest.main()

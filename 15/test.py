#! /usr/bin/env python3

import unittest
from star import calc_hash, one, two

class Test1(unittest.TestCase):
    def testOne(self):
        self.assertEquals(calc_hash("HASH"), 52)
        self.assertEquals(calc_hash("rn=1"), 30)


class Test2(unittest.TestCase):
    def testTwo(self):
        pass

if __name__ == '__main__':
    unittest.main()

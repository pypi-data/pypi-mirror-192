from funlib import math
import unittest
import random


class TestBitshift(unittest.TestCase):

    def test(self):

        for i in range(1000):
            for d in range(1, 4):
                c = [random.randint(0, 100000) for _ in range(d)]
                assert math.decode64(math.encode64(c), d) == c

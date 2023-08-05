from funlib import math
import unittest
import random


class TestCantor(unittest.TestCase):

    def test_1d(self):

        for i in range(1000):
            assert math.cantor_number((i,)) == i

    def test_2d(self):

        for i, x in enumerate([
                  (0, 0),
                  (0, 1),
                  (1, 0),
                  (0, 2),
                  (1, 1),
                  (2, 0),
                  (0, 3),
                  (1, 2),
                  (2, 1),
                  (3, 0)]):
            assert math.cantor_number(x) == i

    def test_4d(self):

        for i, x in enumerate([

                  (0, 0, 0, 0),

                  (0, 0, 0, 1),
                  (0, 0, 1, 0),
                  (0, 1, 0, 0),
                  (1, 0, 0, 0),

                  (0, 0, 0, 2),
                  (0, 0, 1, 1),
                  (0, 1, 0, 1),
                  (1, 0, 0, 1),
                  (0, 0, 2, 0),
                  (0, 1, 1, 0),
                  (1, 0, 1, 0),
                  (0, 2, 0, 0),
                  (1, 1, 0, 0),
                  (2, 0, 0, 0),

                  (0, 0, 0, 3),
                  (0, 0, 1, 2),
                  (0, 1, 0, 2),
                  (1, 0, 0, 2),
                  (0, 0, 2, 1)]):

            assert math.cantor_number(x) == i

    def test_inverse(self, max_val=1000000000, dims=3):
        for i in range(1000):
            coord = [random.randint(0, max_val) for x in range(dims)]
            assert coord == math.inv_cantor_number(
                    math.cantor_number(coord), dims)

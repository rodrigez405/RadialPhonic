import unittest

import numpy as np

from radialphonic import poly_centroid, line_intersect


class TestRadialphonic(unittest.TestCase):
    def setUp(self):
        self.square = [[0, 0], [1, 0], [1, 1], [0, 1]]
        self.eqtri = [[0, 0], [1, 0], [1/2, np.sqrt(3)/2]]

    def test_poly_centroid(self):
        cx, cy = poly_centroid(self.square)
        self.assertAlmostEqual(cx, 0.5, 7, 'wrong x-centroid for a square')
        self.assertAlmostEqual(cy, 0.5, 7, 'wrong y-centroid for a square')

        cx, cy = poly_centroid(self.eqtri)
        self.assertAlmostEqual(cx, 0.5, 7,
                               'wrong x-centroid for an equilateral triangle')
        self.assertAlmostEqual(cy, np.sqrt(3)/6, 7,
                               'wrong y-centroid for an equilateral triangle')

    def test_line_intersect_cross(self):
        ix, iy = line_intersect((0.0, 0.0), (2.0, 0.0), (0.5, -0.5), (0.5, 0.5))
        self.assertAlmostEqual(ix, 0.5, 7,
                               'wrong x-intersection point for cross')
        self.assertAlmostEqual(iy, 0.0, 7,
                               'wrong y-intersection point for cross')

    def test_line_intersect_order_independent(self):
        a1 = (0.0, 0.0)
        a2 = (2.0, 0.0)
        b1 = (0.5, -0.5)
        b2 = (0.5, 0.5)
        hit1 = line_intersect(a1, a2, b1, b2)
        hit2 = line_intersect(b1, b2, a1, a2)
        self.assertEqual(hit1[0], hit2[0],
                         'order of line segment points should not matter')
        self.assertEqual(hit1[1], hit2[1],
                         'order of line segment points should not matter')

    def test_line_intersect_t(self):
        ix, iy = line_intersect((0, 0), (0, 2), (-1, 1), (0, 1))
        self.assertAlmostEqual(ix, 0, 7,
                               'wrong x-intersection point for shared point')
        self.assertAlmostEqual(iy, 1, 7,
                               'wrong y-intersection point for shared point')

    def test_line_intersect_miss(self):
        with self.assertRaises(ArithmeticError):
            line_intersect((0, 0), (0, 2), (2, 1), (0, 3))


"""
Inspired from: http://1ucasvb.tumblr.com/post/42881722643/the-familiar-trigonometric-functions-can-be

Given an arbitrary polygon, first identify the bottom and top boundaries and set
those to -/+ range with midpoint equal to zero. Next, find the centroid of the
polygon and sweep a ray from the center to the edge, producing a sample value.
Determine one period of the shape, then convert that into an audio tone.

Note, the reverse should also be doable - i.e. given a single period of a pure
tone, create the polygon that represents it

e.g.
 A circle will produce a sin wave
 Regular polygons will create tones approaching a pure sin wave as the number
 of sides increases. What about irregular concave or convex polygons?
"""
import matplotlib.pyplot as plt
import numpy as np


def line_intersect(a1, a2, b1, b2):
    """
    http://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
    """
    points = np.vstack((a1, a2, b1, b2))
    p = points[0]
    r = points[1] - points[0]
    q = points[2]
    s = points[3] - points[2]

    alpha = np.cross(q - p, s)
    beta = np.cross(q - p, r)
    delta = np.cross(r, s)

    if delta == 0:
        if alpha == 0:
            raise ArithmeticError('Line segments are collinear')
        else:
            raise ArithmeticError('Line segments are parallel')
    else:
        t = alpha / delta
        u = beta / delta
        if 0 <= t <= 1 and 0 <= u <= 1:
            return p + t*r
        else:
            raise ArithmeticError('Line segments do not intersect')


def poly_centroid(points):
    _points = np.vstack((points, points[0]))
    x, y, area = 0, 0, 0
    for p1, p2 in zip(_points[:-1], _points[1:]):
        c = p1[0]*p2[1] - p2[0]*p1[1]
        area += c
        x += (p1[0] + p2[0]) * c
        y += (p1[1] + p2[1]) * c
    return np.array([x / (3*area), y / (3*area)])


if __name__ == '__main__':
    np.set_printoptions(precision=2)
    # polygon = np.array([[0.0, 0.0], [1, 0], [1, 1], [0, 1]])
    # polygon = np.array([[0, 0], [1, 0], [1/2, np.sqrt(3)/2]])
    polygon = np.array([[1, 3], [-1, 4], [-2, 0], [2, 0], [3, 1.0]])
    centroid = poly_centroid(polygon)
    print(centroid)
    polygon -= centroid

    fs = 1000
    angles = np.linspace(0, 2*np.pi, fs)
    points = np.zeros((len(angles), 2))

    shifts = 0
    segment = polygon[0:2]

    for i, angle in enumerate(angles):
        ray = np.array([10*np.cos(angle), 10*np.sin(angle)])
        hit = None
        while hit is None:
            try:
                hit = line_intersect(segment[0], segment[1], [0, 0], ray)
                points[i] = hit
            except ArithmeticError:
                polygon = np.roll(polygon, -1, axis=0)
                shifts += 1
                segment = polygon[0:2]

                if shifts > 2*len(polygon):
                    raise RuntimeError('Polygon not closed')

    plt.plot(points[:, 1])
    plt.show()

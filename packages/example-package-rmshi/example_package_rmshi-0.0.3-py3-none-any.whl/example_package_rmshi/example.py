import math
import time

def geoVecScale(a, mag):
    return [a[0] * mag, a[1] * mag]
def geoVecSubtract(a, b):
    return [a[0] - b[0], a[1] - b[1]]
def geoVecLength(a):
    return math.sqrt(geoVecLengthSquare(a))
def geoVecLengthSquare(a):
    b = [0, 0]
    x = a[0] - b[0]
    y = a[1] - b[1]
    return x * x + y * y
def geoVecDot(a, b):
    origin = [0, 0]
    p = geoVecSubtract(a, origin)
    q = geoVecSubtract(b, origin)
    return p[0] * q[0] + p[1] * q[1]

def check_polyline_smoothness(polyline):
    if len(polyline) < 3:
        return -1
    firstCoord = geoVecScale(polyline[0], math.pi/ 180.0);
    secondCoord = geoVecScale(polyline[1], math.pi/ 180.0);
    thresh =  math.cos((90.0 * math.pi) / 180.0)
    for idx, coord in enumerate(polyline):
        l1 = geoVecSubtract(secondCoord, firstCoord)
        l1 = geoVecScale(l1, 1 / geoVecLength(l1))
        l2 = geoVecSubtract(coord, secondCoord)
        l2 = geoVecScale(l2, 1 / geoVecLength(l2))
        l1[0] = l1[0] * math.cos(firstCoord[1])
        l2[0] = l2[0] * math.cos(firstCoord[1])
        dot_product = geoVecDot(l1, l2)
        if (dot_product < thresh):
            return False
        firstCoord = secondCoord
        secondCoord = coord
    return True


def test2():
    line = []
    for i in range(100):
        line.append([i, i])
    time1 = time.perf_counter()
    for i in range(100):
        check_polyline_smoothness(line)
    time2 = time.perf_counter()
    print(time1, time2, time2 - time1)
    return time2-time1

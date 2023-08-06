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

#allRelations: Record<string, Relation | null | undefined>,
#laneRelations: string[],
#geometryId: string
def validateDuplicateGeometrySharing(allRelations,laneRelations,geometryId):
    # Check to see if there is a duplicate lane relation or too many lane relations that share the same geometries
    if (len(laneRelations) > 2):
    # If more than 2 lane relations share the same geometry, then there is either a mistake in the lane relation
    # or there are some duplicate lane relations.
        return False
    elif (len(laneRelations) == 2):
      # If 2 relations share the same geometry id then we need to check if the relations share at least
      # 1 left and at least 1 right boundary segment.
        relationId1 = laneRelations[0]
        relationId2 = laneRelations[1]
        relation1 = allRelations[relationId1]
        relation2 = allRelations[relationId2]
        if (relation1 == None or relation2 == None):
            return False
        bothLeft = (geometryId in relation1["left"]) and (geometryId in relation2["left"])
        bothRight = (geometryId in relation1["right"]) and (geometryId in relation2["right"])
        if (bothLeft or bothRight):
            return False
    return True

def test_smoothness_runtime():
    line = []
    for i in range(100):
        line.append([i, i])
    time1 = time.perf_counter()
    for i in range(100):
        check_polyline_smoothness(line)
    time2 = time.perf_counter()
    print(time1, time2, time2 - time1)
    return time2-time1

def test_duplicate_runtime():
    allRelations = {"name1": {"left": [], "right": []}, "name2":{"left": [], "right": []}}
    laneRelations = ["name1", "name2"]
    list_geometryIDs = []
    for i in range(1000):
        list_geometryIDs.append(f"id{i}")
    allRelations["name1"]["left"] = list_geometryIDs
    allRelations["name1"]["right"] = list_geometryIDs
    allRelations["name2"]["left"] = list_geometryIDs
    allRelations["name2"]["right"] = list_geometryIDs
    time1 = time.perf_counter()
    for i in range(1000):
        validateDuplicateGeometrySharing(allRelations, laneRelations, list_geometryIDs[i])
    time2 = time.perf_counter()
    print(time1, time2, time2 - time1)
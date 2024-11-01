import random

def generate_points():
    x1, y1 = random.uniform(0, 1), random.uniform(0, 1)
    x2, y2 = random.uniform(0, 1), random.uniform(0, 1)
    return (x1, y1), (x2, y2)

def left(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((-x2 - x1) * (-x2 + x1) / (-y1 + y2) + y1 + y2) / 2

def right(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((2 - x2 - x1) * (-x2 + x1) / (-y1 + y2) + y1 + y2) / 2

def bottom(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((- y1 - y2) *(-y1 + y2) / (-x2 + x1) + x2 + x1) / 2

def top(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((2 - y1 - y2) *(-y1 + y2) / (-x2 + x1) + x2 + x1) / 2

def point(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    minimum = min(x1, 1 - x1, y1, 1 - y1)
    if minimum == x1:
        return (0, left(point1, point2))
    if minimum == 1 - x1:
        return (1, right(point1, point2))
    if minimum == y1:
        return (bottom(point1, point2), 0)
    if minimum == 1 - y1:
        return (top(point1, point2), 0)
    
def score(point):
    x, y = point
    if 0 <= x <= 1 and 0 <= y <= 1:
        return 1
    return 0

a = 0
for k in range(0, 10000000):
    point1, point2 = generate_points()
    perfect = point(point1, point2)
    a += score(perfect)
print(a / 10000000)

"Result: 0.4911538"
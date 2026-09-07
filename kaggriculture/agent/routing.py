def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def move_towards(pos, target):
    x, y = pos
    tx, ty = target
    if x < tx:
        return ['EAST']
    if x > tx:
        return ['WEST']
    if y < ty:
        return ['SOUTH']
    if y > ty:
        return ['NORTH']
    return ['PASS']


def shed_tiles(size):
    h = size // 2
    return [(h-1, h-1), (h, h-1), (h-1, h), (h, h)]


def nearest_shed(pos, size):
    return min(shed_tiles(size), key=lambda p: distance(pos, p))

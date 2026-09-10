def get_coordinates(coord):
    x, y = coord
    return [[x + i, y + j] for i in range(-1, 2) for j in range(-1, 2)]

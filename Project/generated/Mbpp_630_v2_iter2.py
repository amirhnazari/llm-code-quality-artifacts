def get_coordinates(coord):
    x, y = coord
    return [[x + dx, y + dy] for dx in range(-1, 2) for dy in range(-1, 2)]

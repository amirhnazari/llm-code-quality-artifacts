def get_coordinates(coord):
    """
    Extract all the adjacent coordinates of the given coordinate tuple.
    
    :param coord: A tuple representing the coordinate (x, y).
    :return: A list of lists, each containing an adjacent coordinate [x, y].
    """
    x, y = coord
    return [[x + dx, y + dy] for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)]

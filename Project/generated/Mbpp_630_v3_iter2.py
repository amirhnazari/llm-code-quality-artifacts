def get_coordinates(coord):
    """
    Extract all the adjacent coordinates of the given coordinate tuple.
    
    :param coord: A tuple representing the (x, y) coordinates.
    :return: A list of tuples representing all adjacent coordinates.
    """
    x, y = coord
    return [[x + dx, y + dy] for dx in range(-1, 2) for dy in range(-1, 2)]

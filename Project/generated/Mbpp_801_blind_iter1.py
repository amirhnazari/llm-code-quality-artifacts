def test_three_equal(x, y, z):
    """
    Count the number of equal numbers among three given integers.

    :param x: First integer
    :param y: Second integer
    :param z: Third integer
    :return: Number of equal integers (0, 1, or 3)
    """
    return sum(1 for num in [x, y, z] if num == x) if x == y else 2 if x == z else 1 if y == z else 0

def find_solution(a, b, n):
    """
    Find integers x and y that satisfy ax + by = n as a tuple, or return None if no solution exists.
    
    :param a: Coefficient of x
    :param b: Coefficient of y
    :param n: Target value
    :return: Tuple (x, y) if a solution exists, otherwise None
    """
    for x in range(n // a + 1):
        if (n - a * x) % b == 0:
            y = (n - a * x) // b
            return (x, y)
    return None

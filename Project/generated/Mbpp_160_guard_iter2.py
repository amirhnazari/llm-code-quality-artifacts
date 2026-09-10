def find_solution(a, b, n):
    """
    Returns integers x and y that satisfy ax + by = n as a tuple,
    or return None if no solution exists.
    """
    for x in range(n // a + 1):
        if (n - a * x) % b == 0:
            y = (n - a * x) // b
            return (x, y)
    return None

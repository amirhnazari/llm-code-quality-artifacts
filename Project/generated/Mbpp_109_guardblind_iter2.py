def odd_Equivalent(s, n):
    """
    Count numbers with an odd value when rotating a binary string the given number of times.
    
    :param s: Binary string to rotate
    :param n: Number of rotations
    :return: Count of numbers with an odd value after rotations
    """
    return sum(1 for _ in range(n) if int(s, 2) % 2 == 1)

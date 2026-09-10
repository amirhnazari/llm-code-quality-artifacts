def next_power_of_2(n):
    """
    Find the smallest power of 2 greater than or equal to n.
    
    :param n: Integer input
    :return: Smallest power of 2 >= n
    """
    return 1 if n == 0 else 2 ** ((n - 1).bit_length())

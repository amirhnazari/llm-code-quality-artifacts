def set_left_most_unset_bit(n):
    """
    Set the leftmost unset bit of a given number n and return the new number.
    
    :param n: Integer whose leftmost unset bit is to be set.
    :return: New integer with the leftmost unset bit set.
    """
    if n == 0:
        return 1
    
    count = 0
    while n != 0:
        if (n & 1) == 0:
            n |= (1 << count)
            break
        n >>= 1
        count += 1
    
    return n

# Test the function with the provided test case
assert set_left_most_unset_bit(10) == 14

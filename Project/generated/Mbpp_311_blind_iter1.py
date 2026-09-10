def set_left_most_unset_bit(n):
    """
    Set the leftmost unset bit of a given number n and return the new number.
    """
    if n == 0:
        return 1
    while n & 1:
        n >>= 1
    n |= 1
    return n << 1

# Test the function with the provided test case
assert set_left_most_unset_bit(10) == 14

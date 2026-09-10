def find_Rotations(s):
    """
    Find the minimum number of rotations (greater than 0) required to get the same string.
    
    :param s: Input string
    :return: Minimum number of rotations required
    """
    n = len(s)
    for i in range(1, n):
        if s[i:] + s[:i] == s:
            return i
    return n

# Test the function with the provided test case
assert find_Rotations("aaaa") == 1

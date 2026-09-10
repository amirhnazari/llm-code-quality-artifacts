def eulerian_num(n, m):
    """
    Calculate the Eulerian number a(n, m).

    Args:
    n (int): The first parameter of the Eulerian number.
    m (int): The second parameter of the Eulerian number.

    Returns:
    int: The calculated Eulerian number.
    """
    # Base case: If n is equal to m or m is 0, return 1
    if m in (n, 0):
        return 1
    # Recursive relation for Eulerian numbers
    return ((n - m) * eulerian_num(n - 1, m - 1) + (m + 1) * eulerian_num(n - 1, m))

# Test the function with the provided test case
assert eulerian_num(3, 1) == 4

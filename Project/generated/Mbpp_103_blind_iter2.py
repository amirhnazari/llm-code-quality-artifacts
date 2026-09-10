def eulerian_num(n, m):
    """
    Calculate the Eulerian number a(n, m).
    
    Args:
    n (int): The row in the Eulerian triangle.
    m (int): The column in the Eulerian triangle.
    
    Returns:
    int: The Eulerian number a(n, m).
    """
    if m >= n or n == 0:
        return 0
    return ((n - m) * eulerian_num(n - 1, m - 1) + (m + 1) * eulerian_num(n - 1, m))

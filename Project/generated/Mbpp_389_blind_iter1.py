def find_lucas(n):
    """
    Calculate the n'th Lucas number using an iterative approach for simplicity.
    
    Args:
    n (int): The position in the Lucas sequence to compute.
    
    Returns:
    int: The n'th Lucas number.
    """
    if n == 0:
        return 2
    elif n == 1:
        return 1
    a, b = 2, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

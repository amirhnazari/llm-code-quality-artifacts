def find_lucas(n):
    """
    Write a function to find the n'th lucas number.
    
    Args:
    n (int): The position of the Lucas number to find.
    
    Returns:
    int: The n'th Lucas number.
    """
    if n == 0:
        return 2
    elif n == 1:
        return 1
    
    lucas_prev, lucas_curr = 2, 1
    for _ in range(2, n + 1):
        lucas_next = lucas_prev + lucas_curr
        lucas_prev, lucas_curr = lucas_curr, lucas_next
    
    return lucas_curr

# Test the function with the provided test case
assert find_lucas(9) == 76

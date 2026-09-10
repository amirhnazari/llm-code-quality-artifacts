def is_woodall(n):
    """
    Check if the given number is a Woodall number.
    
    Args:
    n (int): The number to check.
    
    Returns:
    bool: True if n is a Woodall number, False otherwise.
    """
    # Check if n is less than 1, as Woodall numbers are greater than 0
    if n < 1:
        return False
    
    x = 1
    while x < n:
        x = (x << 1) - 1
    
    return x == n

# Test the function with the provided test case
assert is_woodall(383) == True

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
    
    # Initialize the variable to store the current number being checked
    x = 1
    
    # Loop until x is greater than or equal to n
    while x < n:
        # Update x to the next Woodall number
        x *= 2
        x -= 1
    
    # Check if x equals n, which means n is a Woodall number
    return x == n

# Test the function with the provided test case
assert is_woodall(383) == True

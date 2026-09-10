def prime_num(n):
    """
    Check if the given integer is a prime number.
    
    Args:
    n (int): The integer to check.
    
    Returns:
    bool: True if n is a prime number, False otherwise.
    """
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Test the function with the provided test case
assert prime_num(13) == True

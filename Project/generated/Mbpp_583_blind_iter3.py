def catalan_number(n):
    """
    Calculate the nth Catalan number using a simple iterative approach.
    
    Args:
    n (int): The position in the Catalan number sequence.
    
    Returns:
    int: The nth Catalan number.
    """
    if n <= 1:
        return 1
    
    result = 0
    for i in range(n):
        result += catalan_number(i) * catalan_number(n - i - 1)
    
    return result

# Test the function with the provided test case
assert catalan_number(10) == 16796

def last_Digit_Factorial(n):
    """
    Return the last digit of the factorial of a given number n.
    
    Args:
    n (int): The number to find the factorial's last digit for.
    
    Returns:
    int: The last digit of the factorial of n.
    """
    if n == 0 or n == 1:
        return 1
    elif n < 5:
        return n
    else:
        return 0

# Test the function with the provided test case
assert last_Digit_Factorial(4) == 4

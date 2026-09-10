def is_woodall(n):
    """
    Check if the given number is a Woodall number.
    
    A Woodall number is of the form n * 2^n - 1 for some integer n >= 1.
    """
    if n < 1:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1

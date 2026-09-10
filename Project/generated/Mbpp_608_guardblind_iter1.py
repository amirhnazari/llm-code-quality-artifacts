def bell_Number(n):
    """
    Calculate the nth Bell number using dynamic programming.
    
    Args:
    n (int): The position of the Bell number to calculate.
    
    Returns:
    int: The nth Bell number.
    """
    if n == 0:
        return 1
    
    # Initialize a list to store Bell numbers
    bell = [0] * (n + 1)
    bell[0] = 1
    
    for i in range(1, n + 1):
        # Calculate the next Bell number using the previous one
        bell[i] = sum(bell[j] for j in range(i))
    
    return bell[n]

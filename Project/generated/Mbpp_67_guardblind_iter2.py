def bell_number(n):
    """
    Calculate the nth Bell number, which represents the number of ways to partition a set.
    
    Args:
    n (int): The position in the Bell number sequence.
    
    Returns:
    int: The nth Bell number.
    """
    if n == 0:
        return 1
    bell = [0] * (n + 1)
    bell[0] = 1
    for i in range(1, n + 1):
        bell[i] = sum(bell[j] for j in range(i))
    return bell[n]

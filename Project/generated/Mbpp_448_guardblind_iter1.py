def cal_sum(n):
    """
    Calculate the sum of Perrin numbers up to n.
    
    Args:
    n (int): The upper limit for calculating Perrin numbers.
    
    Returns:
    int: The sum of Perrin numbers up to n.
    """
    if n == 0:
        return 3
    elif n == 1:
        return 5
    p, q, r = 3, 0, 2
    total_sum = 5
    for _ in range(3, n + 1):
        next_val = p + q
        total_sum += next_val
        p, q, r = q, r, next_val
    return total_sum

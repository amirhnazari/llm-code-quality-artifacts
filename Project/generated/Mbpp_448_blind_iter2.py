def cal_sum(n):
    """
    Calculate the sum of Perrin numbers up to n.
    
    Args:
    n (int): The number of terms in the Perrin sequence to sum.
    
    Returns:
    int: The sum of the first n Perrin numbers.
    """
    if n == 0:
        return 3
    elif n == 1:
        return 5
    elif n == 2:
        return 7
    
    p, q, r = 3, 0, 2
    total_sum = 5
    
    for _ in range(3, n):
        next_term = p + q
        total_sum += next_term
        p, q, r = q, r, next_term
    
    return total_sum

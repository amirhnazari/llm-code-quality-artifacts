def sequence(n):
    """
    Calculate the nth number in the Newman-Conway sequence.
    
    Args:
    n (int): The position in the sequence to compute.
    
    Returns:
    int: The nth number in the Newman-Conway sequence.
    """
    if n == 1 or n == 2:
        return 1
    return sequence(sequence(n - 1)) + sequence(n - sequence(n - 1))

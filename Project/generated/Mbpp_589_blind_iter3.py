def perfect_squares(start, end):
    """
    Return a list of perfect squares between two given numbers.
    
    Args:
    start (int): The starting number.
    end (int): The ending number.
    
    Returns:
    list: A list of perfect squares within the range [start, end].
    """
    return [x**2 for x in range(start, end + 1) if int(x**0.5)**2 == x**2]

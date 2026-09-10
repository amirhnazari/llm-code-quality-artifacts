def sum_Of_product(n):
    """
    Calculate the sum of the product of consecutive binomial coefficients for a given n.
    
    Args:
    n (int): The upper limit for the binomial coefficients.
    
    Returns:
    int: The sum of the product of consecutive binomial coefficients.
    """
    return sum((i * (n - i)) for i in range(1, n))

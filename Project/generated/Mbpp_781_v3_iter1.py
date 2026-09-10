def count_divisors(n):
    """
    Write a python function to check whether the count of divisors is even.
    
    :param n: Integer to check the number of divisors for
    :return: True if the count of divisors is even, otherwise False
    """
    # Use list comprehension to find all divisors and then check if their count is even
    return len([i for i in range(1, n + 1) if n % i == 0]) % 2 == 0

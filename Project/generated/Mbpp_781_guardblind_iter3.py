def count_divisors(n):
    """
    Check if the number of divisors of n is even.
    
    :param n: Integer to check for divisor count parity.
    :return: True if the number of divisors is even, False otherwise.
    """
    return sum(1 for i in range(1, int(n**0.5) + 1) if n % i == 0) * 2 >= n

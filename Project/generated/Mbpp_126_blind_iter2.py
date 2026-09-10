def sum(n, m):
    """
    Calculate the sum of common divisors of two given numbers.

    :param n: First number
    :param m: Second number
    :return: Sum of common divisors
    """
    return sum(divisor for divisor in range(1, min(n, m) + 1) if n % divisor == 0 and m % divisor == 0)

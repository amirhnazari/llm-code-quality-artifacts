def sumofFactors(n):
    """
    Calculate the sum of even factors of a given number n.
    
    :param n: Integer to find the even factors sum for.
    :return: Sum of even factors of n.
    """
    result = 1  # Initialize result with 1 because it's a factor of all numbers
    i = 2
    while i * i <= n:
        count = 0
        current_sum = 1
        current_term = 1
        while (n % i == 0):
            count += 1
            n //= i
            if (i == 2 and count == 1):
                current_sum = 0  # Reset for the first occurrence of 2
            current_term *= i
            current_sum += current_term
        result *= current_sum
        i += 1
    if n >= 2:
        result *= (1 + n)
    return result

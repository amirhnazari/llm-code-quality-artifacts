def amicable_numbers_sum(limit):
    """
    Sum all amicable numbers up to the given limit.
    
    Amicable numbers are two different numbers so related that the sum of the proper divisors of each is equal to the other number.
    For example, 220 and 284 are amicable because the divisors of 220 are 1, 2, 4, 5, 10, 11, 20, 22, 44, 55, and 110,
    which add up to 284; and the divisors of 284 are 1, 2, 4, 71, and 142, which add up to 220.
    
    :param limit: Upper bound for searching amicable numbers
    :return: Sum of all amicable numbers up to the limit
    """
    def sum_of_divisors(n):
        return sum(i for i in range(1, n) if n % i == 0)
    
    amicable_sum = 0
    for a in range(2, limit + 1):
        b = sum_of_divisors(a)
        if a != b and sum_of_divisors(b) == a:
            amicable_sum += a + b
    return amicable_sum // 2  # Each pair is counted twice

# Test the function with the provided test case
assert amicable_numbers_sum(999) == 504

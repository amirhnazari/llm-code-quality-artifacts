def sum_of_products(n):
    return sum(binomial_coefficient(n, k) * binomial_coefficient(n, k + 1) for k in range(n))

def binomial_coefficient(n, k):
    if k > n - k:
        k = n - k
    return reduce(lambda a, i: a * (n - i) // (i + 1), range(k), 1)

from functools import reduce

# Test the function with the provided test case
assert sum_of_products(3) == 15

def sum_of_products(n):
    """
    Write a python function to find the sum of the product of consecutive binomial coefficients.
    
    :param n: The number of terms in the binomial expansion.
    :return: The sum of the product of consecutive binomial coefficients.
    """
    res = 0
    for k in range(n):
        # Use min to take advantage of symmetry and avoid redundant calculations
        k = min(k, n - k)
        res += (binomial_coefficient(n, k) * binomial_coefficient(n, k + 1))
    return res

def binomial_coefficient(n, k):
    """
    Calculate the binomial coefficient C(n, k).
    
    :param n: The total number of items.
    :param k: The number of items to choose.
    :return: The binomial coefficient.
    """
    if k > n - k:
        k = n - k
    res = 1
    for i in range(k):
        res *= (n - i)
        res //= (i + 1)
    return res

# Test the function with the provided test case
assert sum_of_products(3) == 15

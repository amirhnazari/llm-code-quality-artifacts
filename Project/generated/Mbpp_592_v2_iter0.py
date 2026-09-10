def sum_Of_product(n):
    # Initialize the result variable to store the sum of products
    res = 0
    
    # Iterate through each k from 0 to n-1
    for k in range(0, n):
        # Calculate the product of binomial coefficients C(n, k) and C(n, k+1)
        res += (binomial_coefficient(n, k) * binomial_coefficient(n, k + 1))
    
    return res

def binomial_coefficient(n, k):
    # Initialize the result variable for the binomial coefficient
    res = 1
    
    # If k is greater than n-k to take advantage of symmetry
    if (k > n - k):
        k = n - k
    
    # Calculate the binomial coefficient using a loop
    for i in range(0, k):
        res *= (n - i)
        res //= (i + 1)
    
    return res

# Test the function with the provided test case
assert sum_Of_product(3) == 15

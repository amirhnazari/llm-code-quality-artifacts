def sumofFactors(n): 
    return sum(i for i in range(2, n + 1, 2) if n % i == 0)

# Test the function with the provided test case
assert sumofFactors(18) == 26

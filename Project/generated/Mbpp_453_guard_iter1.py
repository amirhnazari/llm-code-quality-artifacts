def sumofFactors(n): 
    result = sum(i for i in range(1, n + 1) if n % i == 0 and i % 2 == 0)
    return result

# Test the function with the provided test case
assert sumofFactors(18) == 26

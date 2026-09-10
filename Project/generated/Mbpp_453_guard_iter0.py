def sumofFactors(n): 
    result = 0
    i = 1
    while (i <= n): 
        if (n % i == 0): 
            # Check if the factor is even
            if (i % 2 == 0): 
                result += i 
        i += 1
    return result

# Test the function with the provided test case
assert sumofFactors(18) == 26

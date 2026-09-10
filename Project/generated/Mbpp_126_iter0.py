def sum(a, b):
    # Initialize the sum of common divisors
    s = 0
    
    # Iterate through all possible divisors up to the minimum of a and b
    for i in range(1, min(a, b) + 1):
        # Check if both numbers are divisible by the current number
        if (a % i == 0 and b % i == 0):
            s += i
    
    return s

# Test the function with the provided test case
assert sum(10, 15) == 6

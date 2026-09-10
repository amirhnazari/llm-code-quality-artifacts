def sum(a, b):
    """
    Write a python function to find the sum of common divisors of two given numbers.
    """
    # Calculate the greatest common divisor (GCD) of a and b
    gcd = min(a, b)
    while gcd > 0:
        if a % gcd == 0 and b % gcd == 0:
            return gcd
        gcd -= 1

# Test the function with the provided test case
assert sum(10, 15) == 6

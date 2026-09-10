def sum(a, b):
    # Calculate the greatest common divisor (GCD)
    gcd = min(a, b)
    while gcd > 0:
        if a % gcd == 0 and b % gcd == 0:
            return gcd
        gcd -= 1

# Test the function with the provided test case
assert sum(10, 15) == 6

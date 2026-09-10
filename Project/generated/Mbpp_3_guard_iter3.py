def is_not_prime(n):
    """Check if the number is not prime."""
    # Check if the number is less than 2, which is not prime
    if n < 2:
        return True
    # Check for factors from 2 to the square root of n
    return any(n % i == 0 for i in range(2, int(n**0.5) + 1))

# Test the function with the provided test case
assert is_not_prime(2) == False

def is_woodall(n):
    # Check if n is less than 1, as Woodall numbers are greater than 0
    if n < 1:
        return False
    
    x = 1
    while x < n:
        x *= 2
        x -= 1
        if x == n:
            return True
    
    return False

# Test the function with the provided test case
assert is_woodall(383) == True

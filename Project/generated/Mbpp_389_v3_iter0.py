def find_lucas(n):
    # Base cases for the first two Lucas numbers
    if n == 0:
        return 2
    elif n == 1:
        return 1
    
    # Initialize the first two Lucas numbers
    lucas_prev = 2
    lucas_curr = 1
    
    # Calculate the n'th Lucas number using a loop
    for _ in range(2, n + 1):
        lucas_next = lucas_prev + lucas_curr
        lucas_prev = lucas_curr
        lucas_curr = lucas_next
    
    return lucas_curr

# Test the function with the provided test case
assert find_lucas(9) == 76

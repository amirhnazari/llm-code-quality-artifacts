def last_Digit_Factorial(n):
    # Initialize result
    fact = 1
    
    # Multiply numbers from 1 to n and take the last digit of each product
    for i in range(1, n + 1):
        fact = (fact * (i % 10)) % 10
    
    return fact

# Test the function with the provided test case
assert last_Digit_Factorial(4) == 4

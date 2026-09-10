def last_Digit_Factorial(n):
    """
    Write a python function to find the last digit in factorial of a given number.
    
    :param n: The number for which to find the last digit of its factorial.
    :return: The last digit of the factorial of the given number.
    """
    fact = 1
    for i in range(2, n + 1):
        fact = (fact * (i % 10)) % 10
    return fact

# Test the function with the provided test case
assert last_Digit_Factorial(4) == 4

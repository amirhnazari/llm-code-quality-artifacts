def last_digit_factorial(n):
    fact = 1
    for i in range(2, n + 1):
        fact = (fact * (i % 10)) % 10
    return fact

assert last_digit_factorial(4) == 4

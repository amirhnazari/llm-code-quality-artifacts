def count_divisors(n):
    # Initialize a counter for divisors
    c = 0
    
    # Iterate through possible divisors from 1 to n
    for i in range(1, n + 1):
        # Check if i is a divisor of n
        if n % i == 0:
            # Increment the counter if it is a divisor
            c += 1
    
    # Return True if the count of divisors is even, otherwise False
    return (c % 2 == 0)

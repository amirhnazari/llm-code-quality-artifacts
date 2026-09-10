def count_divisors(n):
    # Count divisors using list comprehension and len()
    c = sum(1 for i in range(1, n + 1) if n % i == 0)
    
    # Return True if the count of divisors is even, otherwise False
    return (c % 2 == 0)

def next_power_of_2(n):
    # If n is less than or equal to 1, return 1 as the smallest power of 2
    if (n <= 1):
        return 1
    
    # Initialize p with 0
    p = 0
    
    # Left shift p until it is greater than or equal to n
    while (p < n):
        p = p << 1
    
    # Return the result
    return p

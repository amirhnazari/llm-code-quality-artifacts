def next_power_of_2(n):
    # If n is less than or equal to 1, return 1 as the smallest power of 2
    if n <= 1:
        return 1
    
    # Calculate the position of the highest set bit
    p = (n - 1).bit_length()
    
    # Return 2 raised to the power of p+1
    return 1 << (p + 1)

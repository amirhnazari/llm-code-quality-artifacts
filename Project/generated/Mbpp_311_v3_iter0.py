def set_left_most_unset_bit(n):
    # If n is 0, return 1 as the leftmost unset bit in 0 is at position 0
    if (n == 0):
        return 1
    
    # Initialize count to keep track of the number of bits processed
    count = 0
    
    # Iterate until we find an unset bit from the left
    while (n != 0):
        # If the least significant bit is unset, set it and break the loop
        if ((n & 1) == 0):
            n |= (1 << count)
            break
        
        # Right shift n to check the next bit
        n >>= 1
        count += 1
    
    return n

# Test the function with the provided test case
assert set_left_most_unset_bit(10) == 14

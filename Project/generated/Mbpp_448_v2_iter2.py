def cal_sum(n):
    # Initialize the first three Perrin numbers
    p0, p1, p2 = 3, 0, 2
    
    # Base cases for n < 3
    if n == 0:
        return p0
    elif n == 1:
        return p0 + p1
    elif n == 2:
        return p0 + p1 + p2
    
    # Initialize the sum with the first three Perrin numbers
    total_sum = p0 + p1 + p2
    
    # Calculate the next Perrin numbers and update the sum
    for _ in range(3, n):
        p_next = p0 + p1  # Next Perrin number is the sum of the two preceding ones
        total_sum += p_next  # Add the new Perrin number to the sum
        p0, p1, p2 = p1, p2, p_next  # Update the values for the next iteration
    
    return total_sum

# Test the function with the provided test case
assert cal_sum(9) == 49

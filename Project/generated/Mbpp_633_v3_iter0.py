def pair_xor_Sum(arr, n):
    # Initialize result
    res = 0
    
    # Iterate over all pairs
    for i in range(n):
        for j in range(i + 1, n):
            # Calculate xor of current pair and add to result
            res += (arr[i] ^ arr[j])
    
    return res

# Test the function with the provided test case
assert pair_xor_Sum([5, 9, 7, 6], 4) == 47

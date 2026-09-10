def find_Odd_Pair(arr, n):
    # Initialize count of pairs with odd XOR to 0
    count = 0
    
    # Iterate through each element in the array
    for i in range(n):
        # Compare the current element with all other elements
        for j in range(i + 1, n):
            # Check if the XOR of the pair is odd
            if (arr[i] ^ arr[j]) % 2 != 0:
                count += 1
    
    return count

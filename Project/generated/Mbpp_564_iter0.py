def count_Pairs(arr, n):
    # Initialize a counter for the number of unequal pairs
    cnt = 0
    
    # Iterate through each element in the list
    for i in range(n):
        # Compare the current element with all other elements that come after it
        for j in range(i + 1, n):
            # If the pair is not equal, increment the counter
            if arr[i] != arr[j]:
                cnt += 1
                
    return cnt

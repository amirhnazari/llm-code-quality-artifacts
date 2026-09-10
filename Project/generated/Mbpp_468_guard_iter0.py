def max_product(arr):
    n = len(arr)
    # Initialize the list to store maximum product subsequence ending at each index
    mpis = [0] * n
    
    # The maximum product subsequence ending at the first element is the element itself
    mpis[0] = arr[0]
    
    # Iterate through the array starting from the second element
    for i in range(1, n):
        max_product = 0
        # Check all previous elements to find the maximum product subsequence that can be extended by arr[i]
        for j in range(i):
            if arr[j] < arr[i]:
                max_product = max(max_product, mpis[j])
        
        # The maximum product subsequence ending at arr[i] is either arr[i] itself or arr[i] multiplied by the maximum product subsequence ending at a previous element
        mpis[i] = (max_product * arr[i]) if max_product > 0 else arr[i]
    
    # Return the maximum value from the mpis list, which represents the maximum product of an increasing subsequence
    return max(mpis)

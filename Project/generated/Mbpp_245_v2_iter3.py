def max_sum(arr):
    n = len(arr)
    
    # Initialize arrays for maximum sum of increasing and decreasing subsequences
    inc = arr[:]
    dec = arr[:]
    
    # Fill inc[] with the maximum sum of increasing subsequence ending at each index
    for i in range(1, n):
        inc[i] = max(inc[j] + arr[i] for j in range(i) if arr[i] > arr[j])
    
    # Fill dec[] with the maximum sum of decreasing subsequence starting at each index
    for i in range(n-2, -1, -1):
        dec[i] = max(dec[j] + arr[i] for j in range(i+1, n) if arr[i] > arr[j])
    
    # Find the maximum sum of bitonic subsequence
    return max(inc[i] + dec[i] - arr[i] for i in range(n))

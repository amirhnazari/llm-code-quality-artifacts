def max_sum(arr):
    n = len(arr)
    
    # Initialize the arrays to store maximum sum of increasing and decreasing subsequences
    inc = [0] * n
    dec = [0] * n
    
    # Fill inc[] such that inc[i] contains the maximum sum of increasing subsequence ending with arr[i]
    for i in range(n):
        inc[i] = arr[i]
        for j in range(i):
            if arr[i] > arr[j] and inc[i] < inc[j] + arr[i]:
                inc[i] = inc[j] + arr[i]
    
    # Fill dec[] such that dec[i] contains the maximum sum of decreasing subsequence starting with arr[i]
    for i in range(n-1, -1, -1):
        dec[i] = arr[i]
        for j in range(i+1, n):
            if arr[i] > arr[j] and dec[i] < dec[j] + arr[i]:
                dec[i] = dec[j] + arr[i]
    
    # Find the maximum sum of bitonic subsequence
    max_sum_bitonic = 0
    for i in range(n):
        max_sum_bitonic = max(max_sum_bitonic, inc[i] + dec[i] - arr[i])
    
    return max_sum_bitonic

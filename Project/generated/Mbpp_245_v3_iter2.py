def max_sum(arr):
    n = len(arr)
    
    # Initialize the arrays to store maximum sum of increasing and decreasing subsequences
    inc = [arr[i] for i in range(n)]
    dec = [arr[i] for i in range(n)]
    
    # Fill inc[] such that inc[i] contains the maximum sum of increasing subsequence ending with arr[i]
    for i in range(1, n):
        inc[i] = max((inc[j] + arr[i] for j in range(i) if arr[i] > arr[j]), default=arr[i])
    
    # Fill dec[] such that dec[i] contains the maximum sum of decreasing subsequence starting with arr[i]
    for i in range(n-2, -1, -1):
        dec[i] = max((dec[j] + arr[i] for j in range(i+1, n) if arr[i] > arr[j]), default=arr[i])
    
    # Find the maximum sum of bitonic subsequence
    return max(inc[i] + dec[i] - arr[i] for i in range(n))

def largest_subset(arr):
    n = len(arr)
    arr.sort()
    dp = [1] * n
    
    for i in range(1, n):
        dp[i] = max((dp[j] + 1 if arr[i] % arr[j] == 0 else 1) for j in range(i))
    
    return max(dp)

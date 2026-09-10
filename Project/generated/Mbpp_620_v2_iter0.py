def largest_subset(arr):
    n = len(arr)
    arr.sort()
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] % arr[j] == 0 and dp[i] < dp[j] + 1:
                dp[i] = dp[j] + 1
    
    return max(dp)

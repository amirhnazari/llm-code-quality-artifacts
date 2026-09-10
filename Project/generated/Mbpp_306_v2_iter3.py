def max_sum_increasing_subseq(arr, n, i, k):
    dp = arr[:]
    
    for j in range(1, n):
        if any(arr[x] < arr[j] for x in range(j)):
            dp[j] = max(dp[j], max(dp[:j]) + arr[j])
    
    return max(dp[i], dp[k])

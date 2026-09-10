def max_sum_increasing_subseq(arr, n, i, k):
    dp = [arr[j] for j in range(n)]
    
    for j in range(1, n):
        if arr[j] > arr[j - 1]:
            dp[j] = max(dp[j], dp[j - 1] + arr[j])
    
    return max(dp[i], dp[k])

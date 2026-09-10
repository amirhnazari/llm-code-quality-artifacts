def max_sum_increasing_subseq(arr, n, i, k):
    dp = [arr[j] for j in range(n)]
    
    for j in range(1, n):
        for x in range(j):
            if arr[x] < arr[j]:
                dp[j] = max(dp[j], dp[x] + arr[j])
    
    return max(dp[i], dp[k])

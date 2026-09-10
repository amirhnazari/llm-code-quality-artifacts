def max_sum_increasing_subseq(arr, n, i, k):
    """
    Write a function to find the maximum sum of increasing subsequence from prefix until ith index and also including a given kth element which is after i, i.e., k > i .
    """
    dp = [arr[j] for j in range(n)]
    
    for j in range(1, n):
        for x in range(j):
            if arr[x] < arr[j]:
                dp[j] = max(dp[j], dp[x] + arr[j])
    
    return max(dp[i], dp[k])

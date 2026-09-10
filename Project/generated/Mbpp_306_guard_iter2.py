def max_sum_increasing_subseq(arr, n, i, k):
    """
    Write a function to find the maximum sum of increasing subsequence from prefix until ith index and also including a given kth element which is after i, i.e., k > i .
    """
    dp = [arr[j] for j in range(n)]
    
    for j in range(1, n):
        if arr[j] > arr[j - 1]:
            dp[j] += dp[j - 1]
    
    return max(dp[i], dp[k])

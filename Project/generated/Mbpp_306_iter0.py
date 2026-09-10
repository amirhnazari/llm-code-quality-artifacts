def max_sum_increasing_subseq(arr, n, i, k):
    # Initialize a list to store the maximum sum of increasing subsequence ending at each index
    dp = [0] * n
    
    # Base case: The maximum sum subsequence ending at index 0 is just the element at that index
    dp[0] = arr[0]
    
    # Fill the dp array using dynamic programming
    for j in range(1, n):
        dp[j] = arr[j]
        for x in range(j):
            if (arr[x] < arr[j]) and (dp[j] < dp[x] + arr[j]):
                dp[j] = dp[x] + arr[j]
    
    # Return the maximum sum of increasing subsequence ending at index i including the kth element
    return max(dp[i], dp[k])

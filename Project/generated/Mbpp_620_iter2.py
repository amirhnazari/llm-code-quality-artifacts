def largest_subset(arr):
    """
    Write a function to find the size of the largest subset of a list of numbers so that every pair is divisible.
    
    :param arr: List of integers
    :return: Size of the largest subset
    """
    n = len(arr)
    arr.sort()
    dp = [1] * n
    
    for i in range(1, n):
        dp[i] = max((dp[j] + 1 if arr[i] % arr[j] == 0 else 1) for j in range(i))
    
    return max(dp)

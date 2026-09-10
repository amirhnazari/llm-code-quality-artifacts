def max_sum(arr):
    """
    Find the maximum sum of a bitonic subsequence in the given array.
    
    :param arr: List[int] - The input array.
    :return: int - The maximum sum of the bitonic subsequence.
    """
    n = len(arr)
    inc = [arr[i] for i in range(n)]
    dec = [arr[i] for i in range(n)]
    
    # Compute maximum sum increasing subsequence
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j] and inc[i] < inc[j] + arr[i]:
                inc[i] = inc[j] + arr[i]
    
    # Compute maximum sum decreasing subsequence
    for i in range(n-2, -1, -1):
        for j in range(i+1, n):
            if arr[i] > arr[j] and dec[i] < dec[j] + arr[i]:
                dec[i] = dec[j] + arr[i]
    
    # Find the maximum sum of bitonic subsequence
    max_sum = 0
    for i in range(n):
        max_sum = max(max_sum, inc[i] + dec[i] - arr[i])
    
    return max_sum

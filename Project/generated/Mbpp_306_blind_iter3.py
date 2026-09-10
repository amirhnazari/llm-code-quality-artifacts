def max_sum_increasing_subseq(arr, n, i, k):
    """
    Find the maximum sum of increasing subsequence from prefix until ith index and also including a given kth element which is after i.
    
    :param arr: List of integers representing the array.
    :param n: Integer representing the length of the array.
    :param i: Integer representing the current index.
    :param k: Integer representing the index of the element to include in the subsequence.
    :return: Integer representing the maximum sum of increasing subsequence.
    """
    if arr[i] >= arr[k]:
        return 0
    
    max_sum = arr[i]
    for j in range(i + 1, n):
        if arr[j] > arr[i] and arr[j] < arr[k]:
            max_sum = max(max_sum, arr[i] + max_sum_increasing_subseq(arr, n, j, k))
    
    return max_sum

def max_sub_array_sum(arr, n):
    """
    Find the sum of the largest contiguous sublist in the given list.
    
    :param arr: List of integers
    :param n: Number of elements in the list
    :return: Sum of the largest contiguous sublist
    """
    max_so_far = float('-inf')
    max_ending_here = 0
    
    for i in range(n):
        max_ending_here += arr[i]
        if max_so_far < max_ending_here:
            max_so_far = max_ending_here
        if max_ending_here < 0:
            max_ending_here = 0
            
    return max_so_far

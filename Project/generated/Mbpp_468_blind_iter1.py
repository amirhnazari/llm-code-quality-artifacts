def max_product(arr):
    """
    Find the maximum product of an increasing subsequence in the array.
    
    :param arr: List of integers
    :return: Maximum product of an increasing subsequence
    """
    n = len(arr)
    if n == 0:
        return 0
    
    # Initialize the list to store the maximum product subsequence ending at each index
    max_product_subseq = arr[:]
    
    # Fill max_product_subseq such that max_product_subseq[i] contains the maximum product of an increasing subsequence ending with arr[i]
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j] and max_product_subseq[i] < max_product_subseq[j] * arr[i]:
                max_product_subseq[i] = max_product_subseq[j] * arr[i]
    
    # The maximum value in max_product_subseq is the answer
    return max(max_product_subseq)

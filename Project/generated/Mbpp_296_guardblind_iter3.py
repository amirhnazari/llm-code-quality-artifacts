def get_Inv_Count(arr):
    """
    Count the number of inversions in an array using a more efficient approach.
    
    :param arr: List of integers
    :return: Number of inversions
    """
    return sum(1 for i in range(len(arr)) for j in range(i + 1, len(arr)) if arr[i] > arr[j])

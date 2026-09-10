def check_min_heap(arr):
    """
    Check if the given array represents a min heap.
    
    Args:
    arr (list): The list to be checked.
    
    Returns:
    bool: True if the list is a min heap, False otherwise.
    """
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        if 2 * i + 2 < n and arr[i] > arr[2 * i + 2]:
            return False
        if 2 * i + 1 < n and arr[i] > arr[2 * i + 1]:
            return False
    return True

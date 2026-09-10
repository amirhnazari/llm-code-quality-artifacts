def find_first_occurrence(arr, target):
    """
    Find the index of the first occurrence of a given number in a sorted array.
    
    :param arr: List[int] - A sorted list of integers.
    :param target: int - The target integer to find.
    :return: int - The index of the first occurrence of the target, or -1 if not found.
    """
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid
            right = mid - 1
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result

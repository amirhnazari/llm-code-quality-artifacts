def find_first_occurrence(arr, x):
    """
    Write a function to find the index of the first occurrence of a given number in a sorted array.
    
    :param arr: List[int] - A sorted list of integers.
    :param x: int - The target integer to find.
    :return: int - The index of the first occurrence of x in arr, or -1 if not found.
    """
    l, r = 0, len(arr) - 1
    while l <= r:
        mid = (l + r) // 2
        if arr[mid] < x:
            l = mid + 1
        elif arr[mid] > x:
            r = mid - 1
        else:
            if mid == 0 or arr[mid - 1] != x:
                return mid
            r = mid - 1
    return -1

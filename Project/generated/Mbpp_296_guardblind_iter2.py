def get_Inv_Count(arr):
    """
    Count the number of inversions in an array using a more efficient approach.
    
    :param arr: List of integers
    :return: Number of inversions
    """
    n = len(arr)
    inv_count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                inv_count += 1
    return inv_count

# Test the function with the provided test case
assert get_Inv_Count([1, 20, 6, 4, 5]) == 5

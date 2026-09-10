def comb_sort(arr):
    """
    Sorts an array using the Comb Sort algorithm.
    
    Args:
    arr (list): The list of elements to be sorted.
    
    Returns:
    list: The sorted list.
    """
    gap = len(arr)
    shrink_factor = 1.3
    is_sorted = False

    while not is_sorted or gap > 1:
        if gap > 1:
            gap = int(gap / shrink_factor)

        is_sorted = True
        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                is_sorted = False

    return arr

# Test the function with the provided test case
assert comb_sort([5, 15, 37, 25, 79]) == [5, 15, 25, 37, 79]

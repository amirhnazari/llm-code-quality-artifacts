def find_min_diff(arr, n):
    """
    Find the minimum difference between any two elements in a given array.
    
    :param arr: Array of integers
    :param n: Number of elements in the array
    :return: Minimum difference between any two elements
    """
    arr.sort()
    min_diff = float('inf')
    for i in range(1, n):
        diff = arr[i] - arr[i-1]
        if diff < min_diff:
            min_diff = diff
    return min_diff

# Test the function with the provided test case
assert find_min_diff((1, 5, 3, 19, 18, 25), 6) == 1

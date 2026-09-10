def find_min_diff(arr, n):
    # Sort the array to make it easier to find the minimum difference
    arr.sort()
    
    # Initialize the minimum difference with a large number
    min_diff = float('inf')
    
    # Iterate through the sorted array and calculate differences between consecutive elements
    for i in range(1, n):
        diff = arr[i] - arr[i-1]
        if diff < min_diff:
            min_diff = diff
    
    return min_diff

# Test the function with the provided test case
assert find_min_diff((1, 5, 3, 19, 18, 25), 6) == 1

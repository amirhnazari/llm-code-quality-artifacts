def check_min_heap(arr):
    # Iterate over each node in the array except the last one (since it's a complete binary tree)
    for i in range(len(arr) // 2):
        if arr[i] > min(arr[2 * i + 1], arr[2 * i + 2]):
            return False
    return True

# Test the function with the provided test case
assert check_min_heap([1, 2, 3, 4, 5, 6]) == True

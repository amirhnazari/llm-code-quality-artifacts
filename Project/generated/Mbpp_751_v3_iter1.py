def check_min_heap(arr):
    # Iterate over each node in the array except the last one (since it's a complete binary tree)
    for i in range(len(arr) // 2):
        # Check if the current node is greater than its left child or right child
        if arr[i] > arr[2 * i + 1] or (2 * i + 2 < len(arr) and arr[i] > arr[2 * i + 2]):
            return False
    return True

# Test the function with the provided test case
assert check_min_heap([1, 2, 3, 4, 5, 6]) == True

def check_min_heap(arr):
    return all(arr[i] <= arr[2 * i + 1] and arr[i] <= arr[2 * i + 2] for i in range(len(arr) // 2))

# Test the function with the provided test case
assert check_min_heap([1, 2, 3, 4, 5, 6]) == True

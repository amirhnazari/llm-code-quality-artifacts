def find_min_diff(arr, n):
    arr.sort()
    min_diff = float('inf')
    for i in range(1, n):
        min_diff = min(min_diff, arr[i] - arr[i-1])
    return min_diff

assert find_min_diff((1, 5, 3, 19, 18, 25), 6) == 1

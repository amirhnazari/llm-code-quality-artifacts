def find_min_diff(arr, n):
    arr.sort()
    return min(b - a for a, b in zip(arr, arr[1:]))

assert find_min_diff((1, 5, 3, 19, 18, 25), 6) == 1

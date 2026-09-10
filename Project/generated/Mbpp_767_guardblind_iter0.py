def get_pairs_count(arr, target_sum):
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == target_sum:
                count += 1
    return count

# Test the function with the provided test case
assert get_pairs_count([1, 1, 1, 1], 2) == 6

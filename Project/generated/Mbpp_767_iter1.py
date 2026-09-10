def get_pairs_count(arr, target_sum):
    count = 0
    seen = set()
    for num in arr:
        complement = target_sum - num
        if complement in seen:
            count += seen[complement]
        seen[num] = seen.get(num, 0) + 1
    return count

# Test the function with the provided test case
assert get_pairs_count([1, 1, 1, 1], 2) == 6

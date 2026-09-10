def get_pairs_count(nums, target_sum):
    """
    Count the number of pairs in the list 'nums' that add up to 'target_sum'.
    
    :param nums: List of integers.
    :param target_sum: Integer representing the target sum of pairs.
    :return: Integer count of pairs whose sum equals 'target_sum'.
    """
    num_counts = {}
    for num in nums:
        complement = target_sum - num
        if complement in num_counts:
            num_counts[num] += 1
        else:
            num_counts[num] = 0
    
    pair_count = sum(v * (v + 1) // 2 for v in num_counts.values())
    return pair_count

# Test the function with the provided test case
assert get_pairs_count([1, 1, 1, 1], 2) == 6

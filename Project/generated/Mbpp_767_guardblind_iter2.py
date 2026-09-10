def get_pairs_count(nums, target_sum):
    """
    Count the number of pairs in the list 'nums' that add up to 'target_sum'.
    
    :param nums: List of integers.
    :param target_sum: Integer representing the target sum of pairs.
    :return: Integer count of pairs whose sum equals 'target_sum'.
    """
    num_count = {}
    pair_count = 0
    
    for num in nums:
        complement = target_sum - num
        if complement in num_count:
            pair_count += num_count[complement]
        if num in num_count:
            num_count[num] += 1
        else:
            num_count[num] = 1
            
    return pair_count

from itertools import combinations

def combinations_list(nums):
    result = []
    for i in range(len(nums) + 1):
        for combo in combinations(nums, i):
            result.append(list(combo))
    return result

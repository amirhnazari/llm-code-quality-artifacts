from itertools import combinations

def combinations_list(nums):
    return [list(combo) for i in range(len(nums) + 1) for combo in combinations(nums, i)]

def largest_subset(nums):
    """
    Find the size of the largest subset of numbers where every pair is divisible.
    
    :param nums: List of integers
    :return: Size of the largest such subset
    """
    nums.sort()
    dp = [1] * len(nums)
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[i] % nums[j] == 0:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

# Test the function with the provided test case
assert largest_subset([1, 3, 6, 13, 17, 18]) == 4

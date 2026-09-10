def pair_xor_sum(arr):
    """
    Write a python function to find the sum of xor of all pairs of numbers in the given list.
    
    :param arr: List of integers
    :return: Sum of XOR of all pairs
    """
    return sum(x ^ y for i, x in enumerate(arr) for j, y in enumerate(arr) if i < j)

# Test the function with the provided test case
assert pair_xor_sum([5, 9, 7, 6]) == 47

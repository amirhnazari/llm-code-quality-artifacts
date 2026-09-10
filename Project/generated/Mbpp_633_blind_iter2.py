def pair_xor_Sum(arr, n):
    """
    Calculate the sum of XOR for all pairs in the given list.

    :param arr: List of integers.
    :param n: Number of elements in the list.
    :return: Sum of XOR of all pairs.
    """
    xor_sum = 0
    for i in range(n):
        xor_sum += (arr[i] << (n - i - 1)) * ((1 << i) - 1)
    return xor_sum

# Test the function with the provided test case
assert pair_xor_Sum([5, 9, 7, 6], 4) == 47

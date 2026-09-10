def pair_xor_sum(arr):
    return sum(x ^ y for x in arr for y in arr if x != y)

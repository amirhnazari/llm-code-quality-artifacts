def pair_xor_sum(arr):
    return sum(x ^ y for i, x in enumerate(arr) for j, y in enumerate(arr) if i < j)

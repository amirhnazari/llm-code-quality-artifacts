def count_Pairs(arr):
    total_pairs = len(arr) * (len(arr) - 1) // 2
    unique_counts = {x: arr.count(x) for x in set(arr)}
    equal_pairs = sum(v * (v - 1) // 2 for v in unique_counts.values())
    return total_pairs - equal_pairs

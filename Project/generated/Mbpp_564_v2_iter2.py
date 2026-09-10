def count_Pairs(arr):
    return len(arr) * (len(arr) - 1) // 2 - sum(arr.count(x) * (arr.count(x) - 1) // 2 for x in set(arr))

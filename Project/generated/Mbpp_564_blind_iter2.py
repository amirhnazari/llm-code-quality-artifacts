def count_Pairs(arr, n):
    """
    Count the number of unordered pairs (i, j) such that arr[i] != arr[j].
    
    :param arr: List of integers.
    :param n: Number of elements in the list.
    :return: Number of unordered pairs with unequal elements.
    """
    return n * (n - 1) // 2 - sum(arr.count(x) * (arr.count(x) - 1) // 2 for x in set(arr))

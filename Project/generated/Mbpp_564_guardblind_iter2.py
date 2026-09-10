def count_Pairs(arr, n):
    """
    Count the number of unordered pairs (i, j) such that arr[i] != arr[j].
    
    :param arr: List of integers.
    :param n: Number of elements in the list.
    :return: Number of unordered pairs with unequal elements.
    """
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] != arr[j]:
                count += 1
    return count

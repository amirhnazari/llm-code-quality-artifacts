def find_Odd_Pair(arr, n):
    """
    Count the number of pairs whose XOR value is odd.

    :param arr: List of integers.
    :param n: Number of elements in the list.
    :return: Count of pairs with an odd XOR value.
    """
    return sum(1 for i in range(n) for j in range(i + 1, n) if (arr[i] ^ arr[j]) % 2 != 0)

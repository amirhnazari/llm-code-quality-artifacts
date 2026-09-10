def get_median(arr1, arr2, n):
    """
    Write a function to find the median of two sorted lists of same size.
    
    :param arr1: First sorted list
    :param arr2: Second sorted list
    :param n: Size of each list
    :return: Median of the merged and sorted list
    """
    # Merge the two arrays and sort them
    merged = sorted(arr1 + arr2)
    
    # Find the median of the merged array
    if n % 2 == 0:
        return (merged[n // 2 - 1] + merged[n // 2]) / 2.0
    else:
        return float(merged[n // 2])

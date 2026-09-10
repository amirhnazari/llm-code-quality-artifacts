def get_median(arr1, arr2, n):
    """
    Find the median of two sorted arrays of equal size.
    
    :param arr1: First sorted array
    :param arr2: Second sorted array
    :param n: Size of each array
    :return: Median of the two arrays
    """
    i = j = 0
    m1 = m2 = -1
    
    # Find median in first half
    for _ in range(n):
        m2 = m1
        if i < n and j < n:
            if arr1[i] <= arr2[j]:
                m1 = arr1[i]
                i += 1
            else:
                m1 = arr2[j]
                j += 1
        elif i < n:
            m1 = arr1[i]
            i += 1
        else:
            m1 = arr2[j]
            j += 1
    
    # Return the median
    return (m1 + m2) / 2.0

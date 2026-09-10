def get_median(arr1, arr2, n):
    # Merge the two arrays and sort them
    merged = sorted(arr1 + arr2)
    
    # Find the median of the merged array
    if n % 2 == 0:
        return (merged[n // 2 - 1] + merged[n // 2]) / 2.0
    else:
        return float(merged[n // 2])

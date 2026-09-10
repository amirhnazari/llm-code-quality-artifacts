def max_product(arr):
    n = len(arr)
    mpis = arr[:]
    
    for i in range(1, n):
        mpis[i] = max(mpis[i], max((mpis[j] * arr[i] for j in range(i) if arr[j] < arr[i]), default=0))
    
    return max(mpis)

def max_product(arr):
    n = len(arr)
    mpis = arr[:]
    
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                mpis[i] = max(mpis[i], mpis[j] * arr[i])
    
    return max(mpis)

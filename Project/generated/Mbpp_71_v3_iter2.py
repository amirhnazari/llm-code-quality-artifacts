def comb_sort(arr):
    gap = len(arr)
    shrink_factor = 1.3

    while True:
        gap = int(gap / shrink_factor)
        if gap <= 1:
            break

        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]

    return arr

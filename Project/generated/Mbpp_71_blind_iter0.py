def comb_sort(arr):
    # Initialize the gap size to the length of the array and shrink factor
    gap = len(arr)
    shrink_factor = 1.3
    sorted = False

    while not sorted:
        # Calculate the new gap size
        gap = int(gap / shrink_factor)

        if gap <= 1:
            gap = 1
            sorted = True  # If gap is 1, we assume the array is sorted

        i = 0
        while i + gap < len(arr):
            # Compare elements and swap if they are in the wrong order
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False  # If a swap was made, the array is not sorted yet
            i += 1

    return arr

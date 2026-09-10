def find_first_occurrence(arr, x):
    l, r = 0, len(arr) - 1
    
    while l <= r:
        mid = (l + r) // 2
        
        if arr[mid] < x:
            l = mid + 1
        elif arr[mid] > x:
            r = mid - 1
        else:
            if mid == 0 or arr[mid - 1] != x:
                return mid
            r = mid - 1
    
    return -1

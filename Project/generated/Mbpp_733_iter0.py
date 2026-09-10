def find_first_occurrence(arr, x):
    # Initialize the left and right pointers for binary search
    l = 0
    r = len(arr) - 1
    
    # Loop until the left pointer is less than or equal to the right pointer
    while l <= r:
        mid = (l + r) // 2
        
        # Check if the middle element is greater than x
        if arr[mid] > x:
            r = mid - 1
        # Check if the middle element is less than x
        elif arr[mid] < x:
            l = mid + 1
        else:
            # If the middle element is equal to x, check for the first occurrence
            if mid == 0 or arr[mid - 1] != x:
                return mid
            else:
                r = mid - 1
    
    # Return -1 if the number is not found in the array
    return -1

def count_Pairs(arr, n):
    """
    Write a python function which takes a list of integers and counts the number of possible unordered pairs where both elements are unequal.
    
    :param arr: List of integers
    :param n: Number of elements in the list
    :return: Number of unordered pairs with unequal elements
    """
    # Initialize a counter for the number of unequal pairs
    cnt = 0
    
    # Use a set to track unique elements and their counts
    element_counts = {}
    
    # Count occurrences of each element
    for num in arr:
        if num in element_counts:
            element_counts[num] += 1
        else:
            element_counts[num] = 1
            
    # Calculate the number of unequal pairs using combinations
    for count in element_counts.values():
        cnt += count * (n - count)
    
    return cnt // 2

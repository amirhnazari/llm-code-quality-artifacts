def count_Pairs(arr, n):
    """
    Write a python function which takes a list of integers and counts the number of possible unordered pairs where both elements are unequal.
    
    :param arr: List of integers
    :param n: Number of elements in the list
    :return: Number of unordered pairs with unequal elements
    """
    # Initialize a counter for the number of unequal pairs
    cnt = 0
    
    # Iterate through each element in the list
    for i in range(n):
        # Compare the current element with all other elements that come after it
        for j in range(i + 1, n):
            # If the pair is not equal, increment the counter
            if arr[i] != arr[j]:
                cnt += 1
                
    return cnt

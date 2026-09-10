def count_first_elements(test_tup):
    # Initialize a counter to keep track of the number of elements before the tuple element
    res = 0
    
    # Iterate through each element in the tuple
    for ele in test_tup:
        # Check if the current element is a tuple
        if isinstance(ele, tuple):
            break
        # Increment the counter if the current element is not a tuple
        res += 1
    
    # Return the count of elements before the tuple element
    return res

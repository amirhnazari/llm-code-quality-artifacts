def recursive_list_sum(lst):
    # Initialize the sum to zero
    total = 0
    
    # Iterate through each element in the list
    for i in lst:
        # If the element is a list, recursively call the function
        if isinstance(i, list):
            total += recursive_list_sum(i)
        else:
            # Otherwise, add the element to the total sum
            total += i
    
    # Return the total sum of all elements
    return total

# Test the function with the provided test case
assert recursive_list_sum(([1, 2, [3,4],[5,6]]))==21

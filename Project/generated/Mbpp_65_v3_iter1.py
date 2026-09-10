def recursive_list_sum(lst):
    """
    Write a function to flatten a list and sum all of its elements.
    
    :param lst: List containing integers or other lists
    :return: Sum of all integers in the flattened list
    """
    # Use list comprehension to flatten the list and sum its elements
    return sum(item for sublist in lst for item in (recursive_list_sum(sublist) if isinstance(sublist, list) else [sublist]))

# Test the function with the provided test case
assert recursive_list_sum(([1, 2, [3,4],[5,6]]))==21

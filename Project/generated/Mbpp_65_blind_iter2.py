def recursive_list_sum(lst):
    """
    Recursively flattens a list and sums all of its elements.
    
    :param lst: List to be flattened and summed
    :return: Sum of all elements in the flattened list
    """
    return sum(item if not isinstance(item, list) else recursive_list_sum(item) for item in lst)

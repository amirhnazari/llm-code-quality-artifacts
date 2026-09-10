def flatten_list(nested_list):
    """
    Flattens a given nested list structure.
    
    Args:
    nested_list (list): The nested list to be flattened.
    
    Returns:
    list: A flat list containing all the elements from the nested list.
    """
    # Use list comprehension to flatten the nested list
    return [item for sublist in nested_list for item in flatten_list(sublist) if isinstance(sublist, list)] + ([nested_list] if not isinstance(nested_list, list) else [])

def flatten_list(nested_list):
    """
    Flatten a given nested list structure.
    
    Args:
    nested_list (list): A potentially nested list of elements.
    
    Returns:
    list: A flat list containing all the elements from the nested list.
    """
    return [item for sublist in nested_list for item in (flatten_list(sublist) if isinstance(sublist, list) else [sublist])]

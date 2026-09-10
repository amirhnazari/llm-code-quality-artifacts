def dict_depth(d):
    """
    Return the depth of a dictionary.
    
    Args:
    d (dict): The dictionary to measure.
    
    Returns:
    int: The depth of the dictionary.
    """
    if isinstance(d, dict) and d:
        return 1 + max(dict_depth(v) for v in d.values())
    return 0

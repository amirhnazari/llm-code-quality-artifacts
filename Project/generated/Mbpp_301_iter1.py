def dict_depth(d):
    """
    Find the depth of a dictionary.

    Args:
        d (dict): The dictionary to find the depth of.

    Returns:
        int: The depth of the dictionary.
    """
    if not isinstance(d, dict) or not d:
        return 0
    return 1 + max(map(dict_depth, filter(lambda v: isinstance(v, dict), d.values())), default=0)

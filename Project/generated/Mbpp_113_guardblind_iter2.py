def check_integer(s):
    """
    Check if the provided string represents an integer.

    Args:
    s (str): The string to check.

    Returns:
    bool: True if the string is an integer, False otherwise.
    """
    return s.lstrip('-+').isdigit()

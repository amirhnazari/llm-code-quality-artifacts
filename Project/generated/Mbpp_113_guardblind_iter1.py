def check_integer(s):
    """
    Check if the input string represents an integer.

    Args:
    s (str): The string to check.

    Returns:
    bool: True if the string is an integer, False otherwise.
    """
    try:
        int(s)
        return True
    except ValueError:
        return False

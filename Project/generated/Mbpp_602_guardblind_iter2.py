def first_repeated_char(s):
    """
    Find the first repeated character in a given string.

    :param s: The input string to search for repeated characters.
    :return: The first repeated character if found, otherwise None.
    """
    seen = set()
    for char in s:
        if char in seen:
            return char
        seen.add(char)
    return None

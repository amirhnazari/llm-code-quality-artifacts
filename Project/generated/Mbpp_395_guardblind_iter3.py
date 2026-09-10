def first_non_repeating_character(s):
    """
    Find the first non-repeated character in a given string.

    :param s: The input string to search.
    :return: The first non-repeated character, or None if all characters repeat.
    """
    char_count = {}
    for char in s:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    
    for char in s:
        if char_count[char] == 1:
            return char
    return None

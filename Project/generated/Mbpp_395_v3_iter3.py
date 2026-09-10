def first_non_repeating_character(s):
    """
    Write a python function to find the first non-repeated character in a given string.
    """
    char_count = {char: s.count(char) for char in set(s)}
    return next((char for char, count in char_count.items() if count == 1), None)

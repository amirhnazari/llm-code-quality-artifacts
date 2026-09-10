def first_repeated_char(s):
    """
    Write a python function to find the first repeated character in a given string.
    
    :param s: The input string to search for repeated characters.
    :return: The first repeated character if found, otherwise None.
    """
    char_index = {}
    
    for i, char in enumerate(s):
        if char in char_index:
            return char
        char_index[char] = i
    
    return None

# Test the function with the provided test case
assert first_repeated_char("abcabc") == "a"

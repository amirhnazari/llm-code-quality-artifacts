def first_repeated_char(s):
    char_index = {}
    for i, char in enumerate(s):
        if char in char_index:
            return char
        char_index[char] = i
    return None

assert first_repeated_char("abcabc") == "a"

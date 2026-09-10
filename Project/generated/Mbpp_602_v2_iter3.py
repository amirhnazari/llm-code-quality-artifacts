def first_repeated_char(s):
    char_index = set()
    for char in s:
        if char in char_index:
            return char
        char_index.add(char)
    return None

assert first_repeated_char("abcabc") == "a"

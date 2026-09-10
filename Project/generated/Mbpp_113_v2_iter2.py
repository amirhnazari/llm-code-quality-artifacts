def check_integer(s):
    # Check if the string is empty
    if not s:
        return False
    # Check if all characters are digits or a leading '-' sign
    for char in s:
        if (char == '-' and s.index(char) == 0) or char.isdigit():
            continue
        else:
            return False
    return True

# Test the function with the provided test case
assert check_integer("python") == False

def check_integer(s):
    # Check if the string is empty
    if len(s) == 0:
        return False
    # Check if all characters in the string are digits or a leading '-' sign
    for i in range(len(s)):
        if (i == 0 and s[i] == '-') or s[i].isdigit():
            continue
        else:
            return False
    return True

# Test the function with the provided test case
assert check_integer("python") == False

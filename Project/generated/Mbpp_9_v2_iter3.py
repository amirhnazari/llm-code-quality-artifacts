def find_Rotations(s):
    for i in range(1, len(s)):
        if s[i:] + s[:i] == s:
            return i
    return len(s)

# Test the function with the provided test case
assert find_Rotations("aaaa") == 1

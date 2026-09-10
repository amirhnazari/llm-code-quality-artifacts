def find_Rotations(s):
    min_rotations = len(s)
    
    for i in range(1, len(s)):
        if s[i:] + s[:i] == s:
            min_rotations = min(min_rotations, i)
    
    return min_rotations

# Test the function with the provided test case
assert find_Rotations("aaaa") == 1

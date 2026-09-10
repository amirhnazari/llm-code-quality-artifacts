def is_Sub_Array(l1, l2):
    """Check if the second list is a sublist of the first list."""
    if not l2:
        return True
    if len(l2) > len(l1):
        return False

    for i in range(len(l1)):
        if l1[i] == l2[0]:
            if l1[i:i+len(l2)] == l2:
                return True
    return False

# Test the function with the provided test case
assert is_Sub_Array([1, 4, 3, 5], [1, 2]) == False

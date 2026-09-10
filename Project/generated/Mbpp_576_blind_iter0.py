def is_Sub_Array(l1, l2):
    # Check if the second list is empty or if it's equal to the first list
    if not l2:
        return True
    elif len(l2) > len(l1):
        return False

    # Iterate through the first list
    for i in range(len(l1)):
        # If the current element of l1 matches the first element of l2
        if l1[i] == l2[0]:
            n = 1
            # Check subsequent elements
            while (n < len(l2)) and (l1[i + n] == l2[n]):
                n += 1

            # If all elements match, return True
            if n == len(l2):
                return True

    # If no matching subarray is found, return False
    return False

# Test the function with the provided test case
assert is_Sub_Array([1, 4, 3, 5], [1, 2]) == False

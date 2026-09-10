def find_length(binary_str):
    """
    Find the maximum difference between the number of 0s and number of 1s in any sub-string of the given binary string.
    
    :param binary_str: A string consisting of '0's and '1's.
    :return: The maximum difference between the count of '0's and '1's in any sub-string.
    """
    max_diff = current_diff = 0
    for char in binary_str:
        # Increment current_diff for '0', decrement for '1'
        current_diff += (2 * (char == '0') - 1)
        # Reset current_diff if it becomes negative
        if current_diff < 0:
            current_diff = 0
        # Update max_diff if the current_diff is greater
        max_diff = max(max_diff, current_diff)
    return max_diff

# Test the function with the provided test case
assert find_length("11000010001") == 6

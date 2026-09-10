def find_Rotations(s):
    """
    Write a python function to find the minimum number of rotations (greater than 0) required to get the same string.
    
    :param s: Input string
    :return: Minimum number of rotations required
    """
    # Concatenate the string with itself to handle rotations
    temp = s + s
    
    # Initialize minimum rotations to a large number
    min_rotations = float('inf')
    
    # Iterate through each possible rotation
    for i in range(1, len(s)):
        # Calculate the number of rotations needed to get back to the original string
        rotations = (len(s) - i + 1)
        
        # Update the minimum rotations if a smaller value is found
        min_rotations = min(min_rotations, rotations)
    
    return min_rotations

# Test the function with the provided test case
assert find_Rotations("aaaa") == 1

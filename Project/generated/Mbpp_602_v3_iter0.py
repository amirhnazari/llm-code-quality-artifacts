def first_repeated_char(s):
    # Create an empty dictionary to store characters and their indices
    char_index = {}
    
    # Iterate over the string with index
    for i, char in enumerate(s):
        # Check if the character is already in the dictionary
        if char in char_index:
            # If it is, return the character as it's the first repeated one
            return char
        else:
            # If not, add the character to the dictionary with its index
            char_index[char] = i
    
    # If no character repeats, return None
    return None

# Test the function with the provided test case
assert first_repeated_char("abcabc") == "a"

def first_non_repeating_character(s):
    # Create a dictionary to store the frequency of each character
    char_count = {char: s.count(char) for char in set(s)}
    
    # Find and return the first non-repeated character
    for char in s:
        if char_count[char] == 1:
            return char
    
    # If no non-repeated character is found, return None
    return None

# Test the function with the provided test case
assert first_non_repeating_character("abcabc") == None

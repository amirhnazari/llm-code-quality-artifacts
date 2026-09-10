def first_non_repeating_character(s):
    # Create a dictionary to store the frequency of each character
    char_count = {}
    
    # Iterate over the string and count the occurrences of each character
    for char in s:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    
    # Iterate over the string again to find the first non-repeated character
    for char in s:
        if char_count[char] == 1:
            return char
    
    # If no non-repeated character is found, return None
    return None

# Test the function with the provided test case
assert first_non_repeating_character("abcabc") == None

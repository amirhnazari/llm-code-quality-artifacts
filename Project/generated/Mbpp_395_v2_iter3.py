def first_non_repeating_character(s):
    # Create a dictionary to store the frequency of each character
    char_count = {}
    for char in s:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    
    # Find and return the first non-repeated character using a generator expression
    return next((char for char in s if char_count[char] == 1), None)

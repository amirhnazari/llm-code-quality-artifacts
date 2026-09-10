def is_samepatterns(colors, patterns):
    # Check if both lists have the same length
    if len(colors) != len(patterns):
        return False
    
    # Create dictionaries to map colors and patterns
    color_map = {}
    pattern_map = {}
    
    # Iterate through the lists to populate the mappings
    for i in range(len(colors)):
        if colors[i] not in color_map:
            color_map[colors[i]] = i
        if patterns[i] not in pattern_map:
            pattern_map[patterns[i]] = i
    
    # Compare the mappings to check if they are the same
    return color_map == pattern_map

# Test the function with the provided test case
assert is_samepatterns(["red", "green", "green"], ["a", "b", "b"]) == True

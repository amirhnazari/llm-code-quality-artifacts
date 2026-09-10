def is_samepatterns(colors, patterns):
    if len(colors) != len(patterns):
        return False
    
    color_map = {color: i for i, color in enumerate(colors)}
    pattern_map = {pattern: i for i, pattern in enumerate(patterns)}
    
    return color_map == pattern_map

# Test the function with the provided test case
assert is_samepatterns(["red", "green", "green"], ["a", "b", "b"]) == True

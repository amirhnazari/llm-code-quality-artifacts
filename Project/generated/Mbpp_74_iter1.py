def is_samepatterns(colors, patterns):
    """
    Check whether the colors follow the sequence given in the patterns array.

    Args:
        colors (list of str): List of color names.
        patterns (list of str): List of pattern symbols.

    Returns:
        bool: True if the colors match the patterns, False otherwise.
    """
    # Check if both lists have the same length
    if len(colors) != len(patterns):
        return False
    
    # Create dictionaries to map colors and patterns
    color_map = {}
    pattern_map = {}
    
    # Iterate through the lists to populate the mappings
    for color, pattern in zip(colors, patterns):
        if color not in color_map:
            color_map[color] = []
        if pattern not in pattern_map:
            pattern_map[pattern] = []
        color_map[color].append(color)
        pattern_map[pattern].append(pattern)
    
    # Compare the mappings to check if they are the same
    return all(len(v) == 1 for v in color_map.values()) and all(len(v) == 1 for v in pattern_map.values())

def is_samepatterns(colors, patterns):
    """
    Check if the colors follow the same sequence as the patterns.

    Args:
    colors (list of str): List of color names.
    patterns (list of str): List of pattern symbols.

    Returns:
    bool: True if colors match the patterns, False otherwise.
    """
    return all(colors[i] == patterns[i] for i in range(len(colors)))

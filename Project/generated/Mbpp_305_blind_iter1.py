def start_withp(words):
    """
    Return the first two words from the list that start with the letter 'p'.
    
    :param words: List of strings containing words.
    :return: A tuple of the first two words starting with 'p'.
    """
    return next((word for word in words if word.startswith('p') or word.startswith('P')) for _ in range(2))

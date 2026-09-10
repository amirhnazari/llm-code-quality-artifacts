def start_withp(words):
    # Filter words that start with 'P' or 'p' using list comprehension
    result = [word for word in words if word[0] == 'P' or word[0] == 'p']
    # Return the first two elements from the filtered list as a tuple
    return (result[0], result[1])

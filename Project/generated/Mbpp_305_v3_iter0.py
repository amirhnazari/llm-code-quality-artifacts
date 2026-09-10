def start_withp(words):
    # Use list comprehension to filter words that start with 'P' or 'p'
    result = [word for word in words if word[0] == 'P' or word[0] == 'p']
    # Return the first two elements from the filtered list as a tuple
    return (result[0], result[1])

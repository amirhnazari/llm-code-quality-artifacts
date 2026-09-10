def get_ludic(n):
    """
    Write a function to get all lucid numbers smaller than or equal to a given integer.
    
    :param n: The upper limit for finding ludic numbers.
    :return: A list of ludic numbers up to n.
    """
    if n < 1:
        return []
    
    ludics = [1, 2]
    index = 0
    
    while ludics[-1] <= n:
        candidate = ludics[index] + 1
        if all(candidate % l != 0 for l in ludics):
            ludics.append(candidate)
        index += 1
    
    return ludics[:-1]

# Test the function with the provided test case
assert get_ludic(10) == [1, 2, 3, 5, 7]

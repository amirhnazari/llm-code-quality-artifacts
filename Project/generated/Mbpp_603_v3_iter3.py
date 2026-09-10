def get_ludic(n):
    """
    Write a function to get all lucid numbers smaller than or equal to a given integer.
    
    :param n: The upper limit for finding ludic numbers.
    :return: A list of ludic numbers up to n.
    """
    if n < 1:
        return []
    
    ludics = [1, 2]
    index = 1
    
    while True:
        next_ludic = ludics[index] + ludics[index - 1]
        if next_ludic > n:
            break
        ludics.append(next_ludic)
        index += 1
    
    return ludics

# Test the function with the provided test case
assert get_ludic(10) == [1, 2, 3, 5, 7]

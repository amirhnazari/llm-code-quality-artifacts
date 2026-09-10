def get_ludic(n):
    """
    Return all lucid numbers smaller than or equal to n.
    A lucid number is defined as a prime number.
    """
    if n < 2:
        return []
    
    ludics = list(range(1, n + 1))
    i = 0
    while i * i <= n:
        if ludics[i] != 0:
            for j in range(i * i, n + 1, ludics[i]):
                ludics[j - 1] = 0
        i += 1
    
    return [num for num in ludics if num != 0]

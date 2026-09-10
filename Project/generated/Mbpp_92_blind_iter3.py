def is_undulating(num):
    """
    Check if the given number is undulating (alternates between two digits).
    
    :param num: Integer to check
    :return: True if undulating, False otherwise
    """
    s = str(num)
    return len(s) % 2 == 0 and all(s[i] == s[i + 2] for i in range(0, len(s), 2))

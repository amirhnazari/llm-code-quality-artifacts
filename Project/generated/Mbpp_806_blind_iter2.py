def max_run_uppercase(s):
    """
    Find the maximum run of uppercase characters in the given string.

    :param s: Input string
    :return: Length of the longest run of uppercase characters
    """
    return max(len(list(group)) for _, group in itertools.groupby(s, str.isupper))

def next_smallest_palindrome(n):
    """
    Find and return the next smallest palindrome greater than the given number n.
    """
    for candidate in range(n + 1, 2 * n + 2):
        if str(candidate) == str(candidate)[::-1]:
            return candidate

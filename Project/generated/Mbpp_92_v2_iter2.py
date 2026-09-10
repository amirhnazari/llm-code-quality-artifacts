def is_undulating(n):
    s = str(n)
    if len(s) < 3 or len(s) % 2 != 0:
        return False
    return all(s[i] == s[i - 2] for i in range(2, len(s), 2))

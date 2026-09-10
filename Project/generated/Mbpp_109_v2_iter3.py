def odd_Equivalent(s, n):
    count = s.count('1')
    return len(s) if count % 2 != 0 else (len(s) - count + 1)

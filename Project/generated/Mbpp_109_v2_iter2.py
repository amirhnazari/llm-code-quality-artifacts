def odd_Equivalent(s, n):
    count = s.count('1')
    if count % 2 == 0:
        return len(s)
    return (len(s) - count + 1)

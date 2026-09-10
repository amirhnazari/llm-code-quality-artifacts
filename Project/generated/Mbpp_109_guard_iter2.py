def odd_Equivalent(s, n):
    count = s.count('1')
    if count == 0 or count == len(s):
        return 0
    return (len(s) - count + 1)

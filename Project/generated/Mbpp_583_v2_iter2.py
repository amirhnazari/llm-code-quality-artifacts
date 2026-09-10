def catalan_number(n):
    if n == 0:
        return 1
    
    catalan = [1] * (n + 1)
    
    for i in range(2, n + 1):
        catalan[i] = sum(catalan[j] * catalan[i - j - 1] for j in range(i))
    
    return catalan[n]

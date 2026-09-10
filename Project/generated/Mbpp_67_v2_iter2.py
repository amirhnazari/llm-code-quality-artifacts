def bell_number(n):
    B = [[0] * (n + 1) for _ in range(n + 1)]
    B[0][0] = 1
    
    for i in range(1, n + 1):
        B[i][0] = B[i - 1][i - 1]
        for j in range(1, i + 1):
            B[i][j] = B[i - 1][j - 1] + B[i][j - 1]
    
    return B[n][0]

assert bell_number(2) == 2

def get_total_number_of_sequences(m, n):
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        dp[i][1] = i
    
    for j in range(2, n + 1):
        for i in range(j, m + 1):
            dp[i][j] = dp[i - 1][j] + dp[i // 2][j - 1]
    
    return dp[m][n]

assert get_total_number_of_sequences(10, 4) == 4

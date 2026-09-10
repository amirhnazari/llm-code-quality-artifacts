def maxAverageOfPath(matrix):
    n = len(matrix)
    
    # Initialize a DP table with the same dimensions as the matrix
    dp = [[0 for _ in range(n)] for _ in range(n)]
    
    # Fill the DP table
    for i in range(n):
        for j in range(n):
            if i == 0 and j == 0:
                dp[i][j] = matrix[0][0]
            elif i == 0:
                dp[i][j] = dp[i][j-1] + matrix[i][j]
            elif j == 0:
                dp[i][j] = dp[i-1][j] + matrix[i][j]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1]) + matrix[i][j]
    
    # Calculate the maximum average
    max_average = dp[n-1][n-1] / (2 * n - 1)
    
    return max_average

def maxAverageOfPath(matrix):
    """
    Find the path with the maximum average cost in a square matrix.
    
    :param matrix: List of lists representing the N*N matrix.
    :return: Maximum average cost as a float.
    """
    n = len(matrix)
    dp = [[0] * n for _ in range(n)]
    dp[0][0] = matrix[0][0]
    
    # Fill the first row
    for j in range(1, n):
        dp[0][j] = dp[0][j-1] + matrix[0][j]
    
    # Fill the first column
    for i in range(1, n):
        dp[i][0] = dp[i-1][0] + matrix[i][0]
    
    # Fill the rest of the DP table
    for i in range(1, n):
        for j in range(1, n):
            dp[i][j] = max(dp[i-1][j], dp[i][j-1]) + matrix[i][j]
    
    # Calculate the maximum average path cost
    max_cost = dp[n-1][n-1]
    num_cells = 2 * (n - 1) + 1
    return max_cost / num_cells

def get_total_number_of_sequences(m, n):
    """
    Write a function that takes in positive integers m and n and finds the number of possible sequences of length n,
    such that each element is a positive integer and is greater than or equal to twice the previous element but less than or equal to m.
    
    :param m: Positive integer representing the maximum value an element in the sequence can have
    :param n: Positive integer representing the length of the sequence
    :return: Number of possible sequences
    """
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        dp[i][1] = i
        for j in range(2, n + 1):
            dp[i][j] = dp[i - 1][j] + (dp[i // 2][j - 1] if i >= 2 else 0)
    
    return dp[m][n]

assert get_total_number_of_sequences(10, 4) == 4

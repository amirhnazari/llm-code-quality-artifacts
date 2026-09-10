def get_total_number_of_sequences(m, n):
    """
    Calculate the number of possible sequences of length n where each element is a positive integer,
    greater than or equal to twice the previous element but less than or equal to m.
    
    :param m: Upper limit for sequence elements (inclusive)
    :param n: Length of the sequence
    :return: Number of valid sequences
    """
    if n == 0:
        return 1
    if m < 2 ** (n - 1):
        return 0
    
    dp = [0] * (m + 1)
    for i in range(1, m + 1):
        dp[i] = sum(dp[max(i // 2, 1):i + 1])
    
    return dp[m]

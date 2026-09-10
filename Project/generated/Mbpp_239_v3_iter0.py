def get_total_number_of_sequences(m, n):
    # Initialize a 2D list with zeros
    dp = [[0 for x in range(n + 1)] for y in range(m + 1)]
    
    # Iterate over each possible value of m
    for i in range(1, m + 1):
        # Iterate over each possible length of the sequence
        for j in range(1, n + 1):
            # If the sequence length is 1, there's only one possibility (the number itself)
            if j == 1:
                dp[i][j] = i
            else:
                # Calculate the number of sequences by summing up the possibilities from previous values
                dp[i][j] = dp[i - 1][j] + dp[i // 2][j - 1]
    
    # Return the total number of sequences for the given m and n
    return dp[m][n]

# Test the function with the provided test case
assert get_total_number_of_sequences(10, 4) == 4

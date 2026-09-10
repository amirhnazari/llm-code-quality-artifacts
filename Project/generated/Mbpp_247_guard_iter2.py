def lps(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    
    # Every single character is a palindrome of length 1
    for i in range(n):
        dp[i][i] = 1
    
    # Fill the table
    for i in range(n - 2, -1, -1):  # Start from the second last character
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i][j - 1], dp[i + 1][j])
    
    # The length of the longest palindromic subsequence is in dp[0][n-1]
    return dp[0][n - 1]

# Test the function with the provided test case
assert lps("TENS FOR TENS") == 5

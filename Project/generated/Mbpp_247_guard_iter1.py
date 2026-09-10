def lps(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    
    # Every single character is a palindrome of length 1
    for i in range(n):
        dp[i][i] = 1
    
    # Fill the table
    for cl in range(2, n + 1):  # cl is the length of the substring
        for i in range(n - cl + 1):
            j = i + cl - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2 if cl > 2 else 2
            else:
                dp[i][j] = max(dp[i][j - 1], dp[i + 1][j])
    
    # The length of the longest palindromic subsequence is in dp[0][n-1]
    return dp[0][n - 1]

# Test the function with the provided test case
assert lps("TENS FOR TENS") == 5

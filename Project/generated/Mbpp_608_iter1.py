def bell_Number(n):
    """
    Calculate the nth Bell number using the Bell triangle method.

    Args:
    n (int): The position of the Bell number to calculate.

    Returns:
    int: The nth Bell number.
    """
    # Initialize the Bell triangle with zeros
    B = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
    
    # The first element of the Bell triangle is always 1
    B[0][0] = 1
    
    # Fill the Bell triangle using the recursive relation
    for i in range(1, n + 1):
        B[i][0] = B[i - 1][i - 1]
        for j in range(1, i + 1):
            B[i][j] = B[i - 1][j - 1] + B[i][j - 1]
    
    # The nth Bell number is the first element of the (n+1)th row
    return B[n][0]

# Test the function with the provided test case
assert bell_Number(2) == 2

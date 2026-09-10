def bell_number(n):
    """
    Calculate the nth Bell number, which represents the number of ways to partition a set.

    Args:
    n (int): The order of the Bell number to calculate.

    Returns:
    int: The nth Bell number.
    """
    # Initialize a 2D list with zeros
    B = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
    
    # Base case: Bell number for n=0 is 1
    B[0][0] = 1
    
    # Fill the matrix using the recursive relation of Bell numbers
    for i in range(1, n + 1):
        B[i][0] = B[i - 1][i - 1]
        for j in range(1, i + 1):
            B[i][j] = B[i - 1][j - 1] + B[i][j - 1]
    
    # The last element of the matrix is the nth Bell number
    return B[n][0]

# Test the function with the provided test case
assert bell_number(2) == 2

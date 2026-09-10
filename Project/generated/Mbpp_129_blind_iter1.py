def magic_square_test(matrix):
    """
    Check if the given matrix is a magic square.
    
    Args:
    matrix (list of list of int): The matrix to check.
    
    Returns:
    bool: True if the matrix is a magic square, False otherwise.
    """
    n = len(matrix)
    target_sum = sum(matrix[0])
    
    # Check rows
    for row in matrix:
        if sum(row) != target_sum:
            return False
    
    # Check columns
    for col in range(n):
        if sum(matrix[row][col] for row in range(n)) != target_sum:
            return False
    
    # Check diagonals
    if sum(matrix[i][i] for i in range(n)) != target_sum or sum(matrix[i][n-1-i] for i in range(n)) != target_sum:
        return False
    
    return True

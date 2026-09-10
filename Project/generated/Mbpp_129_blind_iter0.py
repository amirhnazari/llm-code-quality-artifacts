def magic_square_test(matrix):
    n = len(matrix)
    magic_sum = sum(matrix[0])

    # Check sums of rows
    for row in matrix:
        if sum(row) != magic_sum:
            return False

    # Check sums of columns
    for col in range(n):
        if sum(matrix[row][col] for row in range(n)) != magic_sum:
            return False

    # Check sum of main diagonal
    if sum(matrix[i][i] for i in range(n)) != magic_sum:
        return False

    # Check sum of secondary diagonal
    if sum(matrix[i][n - 1 - i] for i in range(n)) != magic_sum:
        return False

    return True

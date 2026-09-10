def magic_square_test(matrix):
    n = len(matrix)
    magic_sum = sum(matrix[0])

    # Check sums of rows and columns using list comprehensions
    if any(sum(row) != magic_sum for row in matrix) or \
       any(sum(matrix[row][col] for row in range(n)) != magic_sum for col in range(n)):
        return False

    # Check sum of main diagonal
    if sum(matrix[i][i] for i in range(n)) != magic_sum:
        return False

    # Check sum of secondary diagonal
    if sum(matrix[i][n - 1 - i] for i in range(n)) != magic_sum:
        return False

    return True

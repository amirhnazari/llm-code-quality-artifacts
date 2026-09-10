def perfect_squares(start, end):
    # Initialize an empty list to store perfect squares
    perfect_squares = []
    
    # Iterate through the range from start to end (inclusive)
    for num in range(start, end + 1):
        # Check if the number is a perfect square
        if int(num ** 0.5) ** 2 == num:
            # If it is, append it to the list of perfect squares
            perfect_squares.append(num)
    
    # Return the list of perfect squares
    return perfect_squares

# Test the function with the provided test case
assert perfect_squares(1, 30) == [1, 4, 9, 16, 25]

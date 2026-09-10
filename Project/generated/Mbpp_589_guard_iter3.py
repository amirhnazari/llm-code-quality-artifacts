def perfect_squares(start, end):
    """
    Write a function to find perfect squares between two given numbers.
    
    Args:
    start (int): The starting number of the range (inclusive).
    end (int): The ending number of the range (inclusive).
    
    Returns:
    list: A list of perfect squares within the specified range.
    """
    # Use a list comprehension to find perfect squares
    return [num for num in range(start, end + 1) if int(num ** 0.5) ** 2 == num]

# Test the function with the provided test case
assert perfect_squares(1, 30) == [1, 4, 9, 16, 25]

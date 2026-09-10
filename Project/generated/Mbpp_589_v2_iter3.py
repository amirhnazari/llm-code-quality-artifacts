def perfect_squares(start, end):
    # Use list comprehension to find perfect squares in the range
    return [num for num in range(start, end + 1) if int(num ** 0.5) ** 2 == num]

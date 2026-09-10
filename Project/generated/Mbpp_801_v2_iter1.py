def test_three_equal(x, y, z):
    # Count how many times each number appears in the input
    count = sum([x == y, x == z, y == z])
    return count

# Test the function with the provided test case
assert test_three_equal(1, 1, 1) == 3

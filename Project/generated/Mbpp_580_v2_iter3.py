def extract_even(test_tup):
    # Using list comprehension to filter out odd numbers and tuples recursively
    res = tuple(item if isinstance(item, int) and item % 2 == 0 else 
                 extract_even(item) for item in test_tup)
    return res

# Test the function with the provided test case
assert extract_even((4, 5, (7, 6, (2, 4)), 6, 8)) == (4, (6, (2, 4)), 6, 8)

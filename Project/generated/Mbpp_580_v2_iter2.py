def extract_even(test_tup):
    # Using list comprehension to filter out odd numbers and tuples recursively
    res = tuple(ele if isinstance(ele, int) and ele % 2 == 0 else 
                 extract_even(ele) for ele in test_tup)
    return res

# Test the function with the provided test case
assert extract_even((4, 5, (7, 6, (2, 4)), 6, 8)) == (4, (6, (2, 4)), 6, 8)

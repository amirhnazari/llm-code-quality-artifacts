def extract_even(test_tup):
    # Using list comprehension to filter out odd numbers and tuples recursively
    res = tuple([ele for ele in test_tup if isinstance(ele, int) and ele % 2 == 0 or 
                 isinstance(ele, tuple) and all(sub_ele % 2 == 0 for sub_ele in extract_even(ele))])
    return res

# Test the function with the provided test case
assert extract_even((4, 5, (7, 6, (2, 4)), 6, 8)) == (4, (6, (2, 4)), 6, 8)

def extract_even(nested):
    """
    Remove uneven elements in the nested mixed tuple.
    
    :param nested: A nested mixed tuple containing integers and other tuples.
    :return: A new nested tuple with only even elements.
    """
    return tuple(item if isinstance(item, int) and item % 2 == 0 else extract_even(item)
                 for item in nested)

# Test the function with the provided test case
assert extract_even((4, 5, (7, 6, (2, 4)), 6, 8)) == (4, (6, (2, 4)), 6, 8)

def dict_depth(d):
    # Check if the input is a dictionary and not empty
    if isinstance(d, dict) and d:
        # Recursively find the depth of each value in the dictionary
        return 1 + (max(map(dict_depth, d.values())) if any(isinstance(v, dict) for v in d.values()) else 0)
    # Return 0 if the input is not a dictionary or is an empty dictionary
    return 0

# Test the function with the provided test case
assert dict_depth({'a':1, 'b': {'c': {'d': {}}}}) == 4
